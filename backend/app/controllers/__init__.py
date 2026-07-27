from fastapi import APIRouter

from .admin_controller import router as admin_router
from .apikey_controller import router as api_key_router
from .auth_controller import router as auth_router
from .battle_controller import router as battle_router
from .dashboard_controller import router as dashboard_router
from .friend_controller import router as friend_router
from .profile_controller import router as profile_router
from .public import router as public_router
from .sleep_data_controller import router as sleep_data_router
from .today_stats_controller import router as today_stats_router
from .user_controller import router as user_router
from .protocol_controller import router as protocol_router

router = APIRouter()

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(battle_router)
router.include_router(dashboard_router)
router.include_router(friend_router)
router.include_router(profile_router)
router.include_router(sleep_data_router)
router.include_router(today_stats_router)
router.include_router(user_router)
router.include_router(public_router)
router.include_router(api_key_router)
router.include_router(protocol_router)