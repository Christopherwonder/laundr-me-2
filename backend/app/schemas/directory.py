from pydantic import BaseModel
from typing import Optional, List
from app.schemas.profile import Profile


class FreelancerProfile(Profile):
    rating: Optional[float] = None
    reviews: Optional[int] = None
    is_verified_freelancer: bool = False
    availability: Optional[str] = "available"


class SearchResult(BaseModel):
    users: List[Profile]
    freelancers: List[FreelancerProfile]


class SearchQuery(BaseModel):
    term: str


class FilterParams(BaseModel):
    category: Optional[str] = None
    location: Optional[str] = None
    min_rating: Optional[float] = None


class SortParams(BaseModel):
    sort_by: str = "rating"
    # AI Directory Ranking Agent parameters
    rating_weight: float = 1.0
    sentiment_weight: float = 1.0
    activity_weight: float = 1.0
    proximity_weight: float = 1.0
    price_weight: float = 1.0
