import time
from functools import wraps
from app.core.logger import logger

def log_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # try to determine the class name if the function is an instance method
        if args and hasattr(args[0], '__class__'):
            cls_name = args[0].__class__.__name__
            func_name = f"{cls_name}.{func.__name__}"
        else:
            func_name = func.__name__

        logger.info(f"Started {func_name}")
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Exception in {func_name}: {e}", exc_info=True)
            raise
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info(f"Finished {func_name} in {duration:.2f} seconds")
    return wrapper
