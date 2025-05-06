from .start_handler import router as start_router
from .verification_handler import router as verification_router
from .default_handler import router as default_router


def register_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(verification_router)
    dp.include_router(default_router)
