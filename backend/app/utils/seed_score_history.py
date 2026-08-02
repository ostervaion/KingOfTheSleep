from datetime import datetime, timedelta, timezone
from random import choice, randint, random, sample, seed

from core.database import engine
from models import CombatHistory, Protocol, ScoreHistory, SleepData, User, UserProtocol, UserProfile
from services import recalculate_protocol_stats
from sqlmodel import Session, select
from utils.security import hash_password

from core.config import PROTOCOL_NAMES

seed(42)
SCORE_OFFSETS = [0, 3, 6, 9, 12]

def _ensure_users(session: Session, additional_count: int = 20) -> list[User]:
    """
    Busca los usuarios existentes y añade exactamente 'additional_count'
    usuarios nuevos más a la base de datos, garantizando que tengan ID único.
    """
    existing_users = session.exec(select(User)).all()
    existing_usernames = {user.username for user in existing_users}

    total_actual = len(existing_users)
    target_count = total_actual + additional_count

    adjectives = ["aurora", "nova", "velvet", "pixel", "echo", "storm", "lunar", "cosmo", "raven", "ember"]
    nouns = ["wolf", "fox", "hawk", "tiger", "owl", "drake", "shadow", "falcon", "mystic", "nova"]

    new_users_to_add = []

    current_total_virtual = total_actual

    while len(existing_users) < target_count:
        base_name = f"{choice(adjectives)}{choice(nouns)}{current_total_virtual + 1}"
        username = base_name.lower()
        password = username

        if username in existing_usernames:
            current_total_virtual += 1
            continue

        new_user = User(
            username=username,
            password=hash_password(password),
            email=f"{username}@example.com",
            role="user",
            active=True,
        )
        session.add(new_user)
        new_users_to_add.append(new_user)
        existing_usernames.add(username)
        existing_users.append(new_user)  # Lo sumamos al control del bucle
        current_total_virtual += 1

    if new_users_to_add:
        session.commit()
        for user in new_users_to_add:
            session.refresh(user)

    return new_users_to_add


def _ensure_protocols(session: Session) -> list[Protocol]:
    """Crea el catálogo de protocolos si no existe todavía. Devuelve TODOS los protocolos."""
    existing = session.exec(select(Protocol)).all()
    existing_names = {p.name for p in existing}

    new_protocols = []
    for name in PROTOCOL_NAMES:
        if name not in existing_names:
            protocol = Protocol(name=name, global_win_rate=0.0, global_usage=0)
            session.add(protocol)
            new_protocols.append(protocol)

    if new_protocols:
        session.commit()
        for p in new_protocols:
            session.refresh(p)

    return session.exec(select(Protocol)).all()


def _seed_user_protocols(session: Session, users: list[User], protocols: list[Protocol], now: datetime):
    """
    Para cada usuario dado, asigna un uso aleatorio de 2-4 protocolos,
    con fechas que coincidan con el rango de sus ScoreHistory (offsets en SCORE_OFFSETS).
    Deja intencionalmente al menos un día sin uso por protocolo, para poder
    comparar "días usado" vs "días no usado" en el cálculo de impacto.
    """
    if not protocols:
        return

    for user in users:
        chosen_protocols = sample(protocols, k=randint(2, min(4, len(protocols))))
        for protocol in chosen_protocols:
            used_offsets = sample(SCORE_OFFSETS, k=randint(1, len(SCORE_OFFSETS) - 1))
            for offset in used_offsets:
                created_at = now - timedelta(days=offset)
                session.add(
                    UserProtocol(
                        user_id=user.id,
                        protocol_id=protocol.id,
                        created_at=created_at,
                    )
                )

    session.commit()

def _seed_sleep_data(session: Session, users: list[User], now: datetime) -> None:
    """
    Genera un registro de SleepData por cada offset en SCORE_OFFSETS para
    cada usuario dado, con valores aleatorios pero dentro de rangos realistas
    (inspirados en métricas estilo Whoop).
    """
    if not users:
        return

    new_records = []
    for user in users:
        for offset in SCORE_OFFSETS:
            created_at = now - timedelta(days=offset)

            time_in_bed = round(randint(360, 540) / 60, 2)      # 6h-9h en horas
            awake_time = round(randint(5, 45) / 60, 2)          # 5-45 min
            light_sleep = round(randint(90, 240) / 60, 2)       # 1.5h-4h
            slow_wave = round(randint(45, 120) / 60, 2)         # 45min-2h
            rem = round(randint(45, 120) / 60, 2)                # 45min-2h

            new_records.append(
                SleepData(
                    created_at=created_at,
                    user_id=user.id,
                    username=user.username,
                    time_in_bed=time_in_bed,
                    awake_time=awake_time,
                    light_sleep=light_sleep,
                    slow_wave=slow_wave,
                    rem=rem,
                    disturbance=randint(0, 8),
                    baseline=round(randint(700, 900) / 100, 2),  # 7.0h-9.0h necesidad base
                    debt=round(randint(0, 240) / 60, 2),          # 0h-4h de deuda
                    strain=randint(0, 21),
                    nap=round(choice([0, 0, 0, randint(10, 45)]) / 60, 2),
                    respiratory_rate=randint(12, 18),
                    performance=randint(40, 100),
                    consistency=randint(30, 100),
                    efficiency=randint(60, 100),
                )
            )

    session.add_all(new_records)
    session.commit()
    print(f"Se han generado {len(new_records)} registros de SleepData.")

def _seed_combat_history(session: Session, battles_per_user: int = 4) -> None:
    """
    Genera un mínimo de 'battles_per_user' registros de CombatHistory
    POR CADA usuario existente en la base de datos, con fecha de hoy,
    enfrentándolo contra rivales aleatorios.
    """
    all_users = session.exec(select(User)).all()
    if len(all_users) < 2:
        print("No hay suficientes usuarios para generar batallas.")
        return

    today = datetime.now(timezone.utc).date()
    start_of_day = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)

    battles_to_add = []

    for user in all_users:
        opponents_pool = [u for u in all_users if u.id != user.id]

        for _ in range(battles_per_user):
            opponent = choice(opponents_pool)

                    if random() < 0.5:
                winner, loser = user, opponent
            else:
                winner, loser = opponent, user

            random_time = start_of_day + timedelta(
                hours=randint(0, 23), minutes=randint(0, 59), seconds=randint(0, 59)
            )

            battles_to_add.append(
                CombatHistory(
                    winner_user_id=winner.id,
                    loser_user_id=loser.id,
                    created_at=random_time,
                )
            )

    session.add_all(battles_to_add)
    session.commit()
    print(
        f"¡Se han generado {len(battles_to_add)} batallas nuevas para hoy ({today}), "
        f"{battles_per_user} por usuario ({len(all_users)} usuarios)!"
    )

def _seed_user_profiles(session: Session, users: list[User]) -> None:
    """
    Crea un UserProfile para cada usuario de la lista que aún no tenga uno.
    Al ser una relación 1-a-1 (user_id es unique), evitamos duplicados
    comprobando primero cuáles ya existen.
    """
    if not users:
        return
    """
    avatar_options = [
        "avatars/game/default_1.png",
        "avatars/game/default_2.png",
        "avatars/game/default_3.png",
        None,
    ]
    user_avatar_options = [
        "avatars/user/default_1.png",
        "avatars/user/default_2.png",
        None,
    ]
    """
    user_ids = [u.id for u in users]
    existing_profile_user_ids = {
        up.user_id
        for up in session.exec(
            select(UserProfile).where(UserProfile.user_id.in_(user_ids))
        ).all()
    }

    new_profiles = []
    for user in users:
        if user.id in existing_profile_user_ids:
            continue

        new_profiles.append(
            UserProfile(
                user_id=user.id,
                public=choice([True, True, True, False]),  # mayoría públicos
                exp=randint(0, 5000),
            )
        )

    if new_profiles:
        session.add_all(new_profiles)
        session.commit()
        print(f"Se han generado {len(new_profiles)} perfiles de usuario (UserProfile).")
    else:
        print("Todos los usuarios ya tenían UserProfile asignado.")

def seed_score_history(backfill_existing: bool = True):
    with Session(engine) as session:
        CANTIDAD_NUEVOS_USUARIOS = 20
        MINIMO_BATALLAS_HOY = 4

        print("Buscando e insertando nuevos usuarios...")
        usuarios_antes = session.exec(select(User)).all()
        nuevos_usuarios = _ensure_users(session, additional_count=CANTIDAD_NUEVOS_USUARIOS)

        print("Verificando catálogo de protocolos...")
        protocols = _ensure_protocols(session)

        now = datetime.now(timezone.utc)
        sample_scores = [72, 78, 81, 85, 88, 90, 92, 95, 97, 100]

        print(f"Generando historial de puntajes para los {len(nuevos_usuarios)} nuevos usuarios...")
        for user in nuevos_usuarios:
            for i in range(5):
                score = choice(sample_scores)
                elo = randint(1200, 1700)
                created_at = now - timedelta(days=i * 3)

                session.add(
                    ScoreHistory(
                        user_id=user.id,
                        sleep_score=score,
                        elo_score=elo,
                        created_at=created_at,
                    )
                )
        session.commit()

        _seed_user_profiles(session, nuevos_usuarios)
        print(f"Generando datos de sueño (SleepData) para los {len(nuevos_usuarios)} nuevos usuarios...")
        _seed_sleep_data(session, nuevos_usuarios, now)

        print(f"Generando uso de protocolos para los {len(nuevos_usuarios)} nuevos usuarios...")
        _seed_user_protocols(session, nuevos_usuarios, protocols, now)

        if backfill_existing:
            existing_with_no_protocols = []
            existing_with_no_sleep = []
            for user in usuarios_antes:
                has_protocols = session.exec(
                    select(UserProtocol).where(UserProtocol.user_id == user.id)
                ).first()
                if not has_protocols:
                    existing_with_no_protocols.append(user)

                has_sleep = session.exec(
                    select(SleepData).where(SleepData.user_id == user.id)
                ).first()
                if not has_sleep:
                    existing_with_no_sleep.append(user)

            if existing_with_no_protocols:
                print(
                    f"Backfill: generando uso de protocolos para "
                    f"{len(existing_with_no_protocols)} usuarios existentes sin protocolos..."
                )
                _seed_user_protocols(session, existing_with_no_protocols, protocols, now)
            else:
                print("Backfill: todos los usuarios existentes ya tenían protocolos asignados.")

            if existing_with_no_sleep:
                print(
                    f"Backfill: generando SleepData para "
                    f"{len(existing_with_no_sleep)} usuarios existentes sin datos de sueño..."
                )
                _seed_sleep_data(session, existing_with_no_sleep, now)
            else:
                print("Backfill: todos los usuarios existentes ya tenían datos de sueño.")

        print(
            f"¡Seed completado con éxito! Se han acumulado {len(nuevos_usuarios)} usuarios más "
            f"con 5 registros de historial, sleep data y protocolos asignados cada uno."
        )

        print(f"Generando un mínimo de {MINIMO_BATALLAS_HOY} batallas para hoy...")
        _seed_combat_history(session, battles_per_user=MINIMO_BATALLAS_HOY)
        recalculate_protocol_stats(session)


if __name__ == "__main__":
    seed_score_history()