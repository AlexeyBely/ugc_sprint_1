from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from .response_models import Response
from .request_models import FrameAdd
from services_base.composition_services import get_movie_service
from services_base.base_movie import BaseMovieService

router = APIRouter()


@router.post('/add', response_model=Response, 
                description='Add a frame to the movie')
async def add_frame(
    frame: FrameAdd,
    frame_service: BaseMovieService = Depends(get_movie_service),
) -> Response:
    """Add a frame to the movie."""
    user_id = '1111-11111'
    result = await frame_service.add_frame_movie(
        user_id = user_id,
        movie_id = frame.movie_id,
        frame = frame.frame
    )
    return result
