from fastapi import HTTPException, Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from ..models import MovieDB, UserDB
from ..schemas import MovieCreate, Movie, MovieUpdate
from ..database import get_db
from .users import get_current_user

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, db : Session = Depends(get_db),
                  current_user: UserDB = Depends(get_current_user)):

    db_movie = MovieDB(**movie.dict(), owner_id = current_user.id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.get("/", response_model=list[Movie])
def read_movies(skip : int = 0, limit: int =10, db: Session = Depends(get_db)):
    movies = db.query(MovieDB).offset(skip).limit(limit).all()
    return movies



@router.get("/search", response_model=list[Movie])
def search_movies(
    director: str | None = None,
    year: int | None = None,
    min_rating: float | None = None,
    title_contains: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(MovieDB)

    if director:
        query = query.filter(MovieDB.director.ilike(f"%{director}%"))

    if year:
        query = query.filter(MovieDB.year == year)

    if min_rating:
        query = query.filter(MovieDB.rating >= min_rating)

    if title_contains:
        query = query.filter(MovieDB.title.ilike(f"%{title_contains}%"))

    return query.all()


@router.get("/{movie_id}")
def read_movie(movie_id : int, db: Session = Depends(get_db)):
    movie = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
    if not movie:
        raise HTTPException(404,"Movie not found")
    return movie


    
@router.delete("/{movie_id}")
def delete_movie(movie_id : int, db: Session = Depends(get_db),
                  current_user : UserDB = Depends(get_current_user)):
    movie = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
    if not movie:
        raise HTTPException(404, "Movie not found")
    if movie.owner_id != current_user.id:
        raise HTTPException(403, "Forbidden")
    
    db.delete(movie)
    db.commit()
    return {"message" : "Movie deleted succesfully"}

@router.put("/{movie_id}", response_model=Movie)
def update_movie(movie_id : int, updated_data : MovieUpdate, db: Session = Depends(get_db),
                 current_user : UserDB = Depends(get_current_user)):
    movie = db.query(MovieDB).filter(MovieDB.id == movie_id).first()
    if not movie:
        raise HTTPException(404,"Movie not found")
    if movie.owner_id != current_user.id:
        raise HTTPException(403,"Forbidden")
    
    for key,value in updated_data.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

