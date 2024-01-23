from typing import Annotated

from pydantic import BeforeValidator


def return_none_if_empty(value: str | None) -> str | None:
    if value == "":
        return None

    return value


NotEmptyNullableString = Annotated[str | None, BeforeValidator(return_none_if_empty)]
