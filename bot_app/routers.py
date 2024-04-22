from aiogram import Router

from bot_app.handlers import (admin_router, base_commands_router,
                              callback_router, user_reg_router)

main_router = Router()


main_router.include_router(user_reg_router)
main_router.include_router(base_commands_router)
main_router.include_router(callback_router)
main_router.include_router(admin_router)
