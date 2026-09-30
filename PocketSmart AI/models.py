from pydantic import BaseModel
from typing import Optional

class HomeBudgetInput(BaseModel):
    total_budget: float
    num_lights: int = 2
    num_fans: int = 2
    num_furniture: int = 1
    num_dining_tables: int = 1
    has_living_room: bool = True
    has_kitchen: bool = True
    has_bedroom: bool = True
    additional_requirements: Optional[str] = ""

class PartyBudgetInput(BaseModel):
    total_budget: float
    guest_count: int
    event_type: str
    venue_type: str = "home"
    food_preference: str = "veg"
    decoration_theme: Optional[str] = "simple"

class JewelryBudgetInput(BaseModel):
    total_budget: float
    occasion: str
    style_preference: str = "traditional"
    metal_preference: str = "gold"
    additional_requirements: Optional[str] = ""