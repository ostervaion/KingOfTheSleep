from fastapi import APIRouter, Depends, status

from core.database import get_session
from models import (
    SleepData,
    User,
)
from schemas import (
    SleepDataCreate,
    SleepDataPublic,
)
from utils.security import (
    get_current_active_user,
)

router = APIRouter()

@router.post("/sleep-data", response_model=SleepDataPublic, status_code=status.HTTP_201_CREATED)
def create_sleep_data(
    sleep_data: SleepDataCreate,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    new_sleep_data = SleepData(
        time_in_bed=sleep_data.time_in_bed,
        awake_time=sleep_data.awake_time,
        light_sleep=sleep_data.light_sleep,
        slow_wave=sleep_data.slow_wave,
        rem=sleep_data.rem,
        disturbance=sleep_data.disturbance,
        baseline=sleep_data.baseline,
        debt=sleep_data.debt,
        strain=sleep_data.strain,
        nap=sleep_data.nap,
        respiratory_rate=sleep_data.respiratory_rate,
        performance=sleep_data.performance,
        consistency=sleep_data.consistency,
        efficiency=sleep_data.efficiency,
        user_id=current_user.id,
        username=current_user.username,
    )

    session.add(new_sleep_data)
    session.commit()
    session.refresh(new_sleep_data)

    return new_sleep_data