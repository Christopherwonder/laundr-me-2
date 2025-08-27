from fastapi import HTTPException
from app.schemas.profile import Profile
from app.schemas.settings import Settings
from app.schemas.directory import FreelancerProfile, SearchQuery, FilterParams, SortParams
from typing import List

# Dummy databases
db_profiles = {}
db_settings = {}

async def get_profile_by_id(user_id: int) -> Profile:
    if user_id not in db_profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profiles[user_id]


async def get_profile_by_laundr_id(laundr_id: str):
    for profile in db_profiles.values():
        if profile.laundr_id == laundr_id:
            return profile
    return None

async def search_profiles(query: SearchQuery) -> dict:
    users = []
    freelancers = []
    term = query.term.lower()

    for profile in db_profiles.values():
        is_match = (
            term in profile.laundr_id.lower()
            or (profile.headline and term in profile.headline.lower())
            or any(term in skill.lower() for skill in profile.skill_tags)
        )

        if is_match:
            if profile.skill_tags:
                if isinstance(profile, FreelancerProfile):
                    freelancers.append(profile)
                else:
                    freelancers.append(FreelancerProfile(**profile.model_dump()))
            else:
                users.append(profile)

    return {"users": users, "freelancers": freelancers}

async def filter_freelancers(params: FilterParams) -> List[FreelancerProfile]:
    freelancers = [p for p in db_profiles.values() if isinstance(p, FreelancerProfile)]

    if params.category:
        freelancers = [f for f in freelancers if params.category in f.skill_tags]
    if params.location:
        # Location data is not yet available in the Profile model.
        # This will be a future implementation.
        pass
    if params.min_rating:
        freelancers = [f for f in freelancers if f.rating and f.rating >= params.min_rating]

    return freelancers

async def sort_freelancers(params: SortParams) -> List[FreelancerProfile]:
    freelancers = [p for p in db_profiles.values() if isinstance(p, FreelancerProfile)]

    def calculate_score(freelancer: FreelancerProfile):
        score = 0
        # These are dummy values for now, as they are not in the schema
        sentiment = 0.5
        activity = 0.5
        proximity = 0.5
        price = 0.5

        score += (freelancer.rating or 0) * params.rating_weight
        score += sentiment * params.sentiment_weight
        score += activity * params.activity_weight
        score += proximity * params.proximity_weight
        score += price * params.price_weight
        return score

    reverse = True if params.sort_by in ["rating", "score"] else False

    key_func = None
    if params.sort_by == "score":
        key_func = calculate_score
    elif params.sort_by == "rating":
        key_func = lambda f: f.rating or 0
    elif hasattr(FreelancerProfile, params.sort_by):
        key_func = lambda f: getattr(f, params.sort_by) or 0

    if key_func:
        return sorted(freelancers, key=key_func, reverse=reverse)

    return freelancers
