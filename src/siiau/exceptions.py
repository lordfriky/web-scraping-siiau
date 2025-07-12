from typing import Optional
import requests

class SiiauError(Exception):
    def __init__(self, error_message: str) -> None:
        super().__init__(f"Error de SIIAU: {error_message}")

class SiiauDown(SiiauError):
    reason: str
    failed_response: requests.Response | None

    def __init__(self, reason: str, failed_response: Optional[requests.Response] = None) -> None:
        self.reason = reason
        self.failed_response = failed_response
        super().__init__(f"SIIAU parece caído ({reason}).")
