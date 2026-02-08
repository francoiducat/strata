from pydantic import BaseModel


class PortfolioCreateRequest(BaseModel):
    name: str
    base_currency: str = "EUR"

