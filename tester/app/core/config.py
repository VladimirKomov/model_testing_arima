import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    FORWARD_URL: str = os.getenv("FORWARD_URL")
    BACKDOOR_ACCESS_HEADER: str = os.getenv("BACKDOOR_ACCESS_HEADER")
    BACKDOOR_ACCESS_VALUE: str = os.getenv("BACKDOOR_ACCESS_VALUE")

config = Config()