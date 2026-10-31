from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceCreate(BaseModel):
    service_code: str = Field(min_length=4, max_length=10)
    price: float = Field(gt=0, allow_inf_nan=False)
    department_id: int = Field(gt=0)

    @field_validator("service_code")
    @classmethod
    def strip_service_code(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("service_code must not be blank")
        return value


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    service_code: str
    price: float
    department_id: int