from loguru import logger
import sys
import os

# Create a logs folder if it doesn't exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

# Console logs
logger.add(sys.stdout, format="<green>{time}</green> <level>{message}</level>", level="INFO")

# All logs to tester.log (DEBUG and above)
logger.add(
    os.path.join(LOG_DIR, "tester.log"),
    rotation="1 MB",
    level="DEBUG"
)

# Only errors (ERROR and above) to tester_errors.log
logger.add(
    os.path.join(LOG_DIR, "tester_errors.log"),
    rotation="1 MB",
    level="ERROR"
)

__all__ = ["logger"]
