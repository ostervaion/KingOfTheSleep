from datetime import datetime, timedelta, timezone
from random import choice, randint, seed

from sqlmodel import Session, select

from database import engine
from models import ScoreHistory, User
from security import hash_password

# Fijamos la semilla para que los nombres aleatorios sigan un patrón predecible
seed(42)


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


def seed_score_history():
    with Session(engine) as session:
        # Configura aquí cuántos usuarios NUEVOS quieres agregar en cada ejecución
        CANTIDAD_NUEVOS_USUARIOS = 20
        
        print("Buscando e insertando nuevos usuarios...")
        nuevos_usuarios = _ensure_users(session, additional_count=CANTIDAD_NUEVOS_USUARIOS)

        # NOTA: Hemos eliminado 'session.exec(delete(ScoreHistory))' para no borrar
        # el historial acumulado de las ejecuciones anteriores.

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
                        user_id=user.id,  # user.id ahora está garantizado gracias al refresh anterior
                        sleep_score=score,
                        elo_score=elo,
                        created_at=created_at,
                    )
                )

        # Commit definitivo para guardar todos los historiales de los usuarios nuevos
        session.commit()
        print(f"¡Seed completado con éxito! Se han acumulado {len(nuevos_usuarios)} usuarios más con 5 registros de historial cada uno.")


if __name__ == "__main__":
    seed_score_history()