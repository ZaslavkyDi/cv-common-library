from cv_common_library.message_brokers.schemas import BaseMessageSchema
from pydantic import BaseModel

from cv_common_library.schemas.cv_data_storage.candidates_result import CandidatesPageResultSchema


class CandidateResultBodyMessageSchema(BaseModel):
    page_result: CandidatesPageResultSchema
    source: str


class CandidateResultMessageSchema(BaseMessageSchema):
    """
    Message schema example:
    {
        "metadata": {
            "request_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "body": {
            "page_result": {
                "candidates": [
                    {
                        "name": "John Doe",
                        "position": "Software Engineer",
                        "location": "San Francisco, CA",
                        "source": "LinkedIn",
                        "url": "https://www.linkedin.com/in/johndoe/"
                    },
                ],
                "page_number": 1,
            },
            "source": "robotaua"
        }
    }
    """

    body: CandidateResultBodyMessageSchema
