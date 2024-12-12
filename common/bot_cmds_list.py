from aiogram.types import BotCommand

private = [
    BotCommand(command="start", description="перезапустить бота"),
    BotCommand(command="notifications", description="включить/отключить уведомления о погоде"),
    BotCommand(command="location", description="передать свою геопозицию, для определения погоды"),
]
