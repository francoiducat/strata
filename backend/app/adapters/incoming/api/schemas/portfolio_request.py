from pydantic import BaseModel


class PortfolioCreateRequest(BaseModel):
    name: str
    base_currency: str = "EUR"


class PortfolioUpdateRequest(BaseModel):
    name: str
    base_currency: str = "EUR"

