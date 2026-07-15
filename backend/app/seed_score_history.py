from datetime import datetime, timedelta, timezone
from random import choice, randint, sample, seed
from random import choice, random, randint

from sqlmodel import Session, select

from database import engine
from models import Protocol, ScoreHistory, User, UserProtocol, CombatHistory, ScoreHistory, User
from security import hash_password

# Fijamos la semilla para que los nombres aleatorios sigan un patrón predecible
seed(42)

PROTOCOL_NAMES = [
    "Temperature Cycling",
    "Light Management",
    "Stimulant Control",
    "Magnesium Intake",
    "Melatonin Intake",
    "Sunlight Maxing",
    "Caffeine Minimum",
]

# Mismos offsets (en días) usados para generar el ScoreHistory de cada usuario
SCORE_OFFSETS = [0, 3, 6, 9, 12]


def _ensure_users(session: Session, additional_count: int = 20) -> list[User]:
    """
    Busca los usuarios existentes y añade exactamente 'additional_count'
    usuarios nuevos más a la base de datos, garantizando que tengan ID único.
    """
    # 1. Obtener los usuarios que YA existen actualmente en la base de datos
    existing_users = session.exec(select(User)).all()
    existing_usernames = {user.username for user in existing_users}

    # 2. Calcular cuántos usuarios debe haber en total al terminar esta ejecución
    total_actual = len(existing_users)
    target_count = total_actual + additional_count

    adjectives = ["aurora", "nova", "velvet", "pixel", "echo", "storm", "lunar", "cosmo", "raven", "ember"]
    nouns = ["wolf", "fox", "hawk", "tiger", "owl", "drake", "shadow", "falcon", "mystic", "nova"]

    new_users_to_add = []

    # Contador virtual para el sufijo numérico del nombre de usuario
    current_total_virtual = total_actual

    while len(existing_users) < target_count:
        base_name = f"{choice(adjectives)}{choice(nouns)}{current_total_virtual + 1}"
        username = base_name.lower()
        password = username

        # Si por casualidad el username ya existe, saltamos e incrementamos para evitar duplicados
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

    # Un único commit en lote para todos los usuarios nuevos creados en esta tanda
    if new_users_to_add:
        session.commit()
        # Refrescamos los nuevos usuarios para que Postgres les asigne su ID real en memoria
        for user in new_users_to_add:
            session.refresh(user)

    # Devolvemos ÚNICAMENTE los usuarios nuevos que se acaban de crear en esta tanda
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

            # 50/50 de que el usuario actual gane o pierda
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

        print(f"Generando uso de protocolos para los {len(nuevos_usuarios)} nuevos usuarios...")
        _seed_user_protocols(session, nuevos_usuarios, protocols, now)

        if backfill_existing:
            existing_with_no_protocols = []
            for user in usuarios_antes:
                has_protocols = session.exec(
                    select(UserProtocol).where(UserProtocol.user_id == user.id)
                ).first()
                if not has_protocols:
                    existing_with_no_protocols.append(user)

            if existing_with_no_protocols:
                print(
                    f"Backfill: generando uso de protocolos para "
                    f"{len(existing_with_no_protocols)} usuarios existentes sin protocolos..."
                )
                _seed_user_protocols(session, existing_with_no_protocols, protocols, now)
            else:
                print("Backfill: todos los usuarios existentes ya tenían protocolos asignados.")

        print(
            f"¡Seed completado con éxito! Se han acumulado {len(nuevos_usuarios)} usuarios más "
            f"con 5 registros de historial y protocolos asignados cada uno."
        )

        print(f"Generando un mínimo de {MINIMO_BATALLAS_HOY} batallas para hoy...")
        _seed_combat_history(session, battles_per_user=MINIMO_BATALLAS_HOY)


if __name__ == "__main__":
    seed_score_history()