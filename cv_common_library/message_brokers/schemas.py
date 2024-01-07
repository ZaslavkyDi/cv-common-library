from typing import Any

from pydantic import BaseModel, UUID4


class BaseMetadataSchema(BaseModel):
    request_id: UUID4


class BaseMessageSchema(BaseModel):
    metadata: BaseMetadataSchema
    body: Any
