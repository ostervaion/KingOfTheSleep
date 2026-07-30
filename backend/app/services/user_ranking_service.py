from sqlmodel import select

from models import ScoreHistory, User, UserProfile


def build_ranking(session, current_user_id: int):
    all_scores = session.exec(
        select(ScoreHistory)
        .order_by(ScoreHistory.created_at.desc())
    ).all()

    latest_by_user = {}
    previous_by_user = {}

    for score in all_scores:
        if score.user_id is None:
            continue

        if score.user_id not in latest_by_user:
            latest_by_user[score.user_id] = score

        elif score.user_id not in previous_by_user:
            previous_by_user[score.user_id] = score

    users = session.exec(
        select(User)
    ).all()

    profiles = session.exec(
        select(UserProfile)
    ).all()


    profiles_by_user = {
        profile.user_id: profile
        for profile in profiles
    }

    ranking_data = [
        {
            "user_id": user.id,
            "name": user.username,

            "avatar_path": (
                profiles_by_user[user.id].user_avatar_path
                if user.id in profiles_by_user
                else None
            ),
            "experience": (
                profiles_by_user[user.id].exp
                if user.id in profiles_by_user
                else 0
            ),

            "current_points": (
                latest_by_user[user.id].elo_score
                if user.id in latest_by_user
                else 0
            ),

            "previous_points": (
                previous_by_user[user.id].elo_score
                if user.id in previous_by_user
                else 0
            ),
        }
        for user in users
    ]

    ranking_data.sort(
        key=lambda entry: entry["current_points"],
        reverse=True,
    )

    previous_ranking = sorted(
        ranking_data,
        key=lambda entry: entry["previous_points"],
        reverse=True,
    )

    previous_positions = {
        item["user_id"]: index + 1
        for index, item in enumerate(previous_ranking)
    }

    ranking = []
    current_user_ranking = None
    current_user_prev_pos = None

    for index, entry in enumerate(ranking_data):
        current_pos = index + 1

        previous_pos = previous_positions.get(
            entry["user_id"],
            current_pos,
        )

        pos_delta = previous_pos - current_pos

        ranking.append({
            "ranking": str(current_pos),
            "user_id": entry["user_id"],
            "name": entry["name"],
            "experience": entry["experience"],
            "avatar_path": (
                f"/api{entry['avatar_path']}"
                if entry["avatar_path"]
                else None
            ),
            "points": str(entry["current_points"]),
            "posChange": str(abs(pos_delta)),
            "trend": (
                "up"
                if pos_delta > 0
                else "down"
                if pos_delta < 0
                else "same"
            ),
        })

        if entry["user_id"] == current_user_id:
            current_user_ranking = current_pos
            current_user_prev_pos = previous_pos

    return (
        ranking,
        current_user_ranking,
        current_user_prev_pos,
    )