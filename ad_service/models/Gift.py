from uuid import UUID 
from pydantic import BaseModel, ConfigDict

class Gift(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    wishlist_id: UUID
    name: str
