from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    id: int = Field(ge=0)
    username: str
    first_name: str | None
    last_name: str | None

class ServiceCreateSchema(BaseModel):
    service_name: str
    service_cost: int
    service_time: int
