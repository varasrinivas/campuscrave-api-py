from campuscrave_api.schemas import CamelModel


class DishSummary(CamelModel):
    id: int
    name: str
    description: str | None
    price_rupees: int
    category: str
    vegetarian: bool
    stock: int
    emoji: str | None
    prep_minutes: int
    wednesday_special: bool
    sold_so_far: int
