from pydantic import BaseModel

from cv_common_library.schemas.validators import NotEmptyNullableString


class CandidateDetailsSchema(BaseModel):
    cv_url: str
    position: str
    name: str
    compensation: NotEmptyNullableString = None
    age: int | None = None
    location: NotEmptyNullableString = None


class CandidatesPageResultSchema(BaseModel):
    candidates: list[CandidateDetailsSchema]
    page_number: int
