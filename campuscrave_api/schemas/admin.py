from pydantic import Field

from campuscrave_api.schemas import CamelModel


class StockUpdateRequest(CamelModel):
    stock: int = Field(ge=0)
