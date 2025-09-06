from typing import List

from app.crud import filter_freelancers, search_profiles, sort_freelancers
from app.schemas.directory import (
    FilterParams,
    FreelancerProfile,
    SearchQuery,
    SearchResult,
    SortParams,
)
from fastapi import APIRouter

router = APIRouter()


@router.post("/search", response_model=SearchResult)
async def search(query: SearchQuery):
    return await search_profiles(query)


@router.post("/freelancers/filter", response_model=List[FreelancerProfile])
async def filter_freelancers_endpoint(params: FilterParams):
    return await filter_freelancers(params)


@router.post("/freelancers/sort", response_model=List[FreelancerProfile])
async def sort_freelancers_endpoint(params: SortParams):
    return await sort_freelancers(params)
