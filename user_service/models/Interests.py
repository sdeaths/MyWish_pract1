from uuid import UUID 
from pydantic import BaseModel, ConfigDict

class Interests(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    list: str