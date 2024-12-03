from uuid import UUID 
from pydantic import BaseModel, ConfigDict
from typing import List

from ad_service.models.Gift import Gift


class Wishlist(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    gifts: List[Gift]
