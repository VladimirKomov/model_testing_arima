import httpx

from app.core.config import config
from app.core.decorators import log_execution
from app.core.logger import logger

class RequestSender:
    def __init__(self, forward_url: str):
        self.forward_url = forward_url
        self.backdoor_header = config.BACKDOOR_ACCESS_HEADER
        self.backdoor_value = config.BACKDOOR_ACCESS_VALUE

    @log_execution
    async def send(self, payload: dict) -> dict:
        logger.info(f"Sending request to {self.forward_url} with payload: {payload}")

        headers = {
            self.backdoor_header: self.backdoor_value
        }

        try:
            async with httpx.AsyncClient(timeout=3600) as client:
                response = await client.post(
                    self.forward_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                logger.info(f"Response received successfully: status_code={response.status_code}")
                return response.json()
        except httpx.RequestError as e:
            logger.error(f"Request error while sending to {self.forward_url}: {e}")
            return {"error": str(e)}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for URL {self.forward_url}: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.critical(f"Unexpected error while sending request: {e}")
            return {"error": str(e)}
