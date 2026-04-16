from pydantic import Field, BaseModel

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SuccessOutputResponse(BaseDTO):
    message: str = Field(..., description="Mensagem de sucesso da operação")
