from loguru import logger

logger.add("logs.log")
def catch_logs(func,):
    """Декоратор для логгирования."""
    async def log_wrapper(*args, **kwargs):
        logger.info(f"Пришел запрос на эндпоинт {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(str(e))
            raise e
    return log_wrapper