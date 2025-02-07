from typing import Optional

from pydantic import BaseModel

class ConfigResponse(BaseModel):
    status: str
    message: str