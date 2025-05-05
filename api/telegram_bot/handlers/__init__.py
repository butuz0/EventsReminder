from .message_handler import router as message_router


def register_handlers(dp):
    dp.include_router(message_router)