from loguru import logger
import sys
import os

# Create a logs folder if it doesn't exist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()
logger.add(sys.stdout, format="<green>{time}</green> <level>{message}</level>", level="INFO")

# Logs to a file in the logs folder
logger.add(os.path.join(LOG_DIR, "tester.log"), rotation="1 MB", level="DEBUG")

__all__ = ["logger"]