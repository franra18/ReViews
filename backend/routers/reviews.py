from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from jose import jwt

from models.review import ReviewCreate, ReviewResponse
from models.user import UserBase
from dependencies import get_current_user, oauth2_scheme
from core.database import db
from core.config import settings

router = APIRouter(prefix="/reviews", tags=["reviews"])

reviews_collection = db.reviews


def review_helper(review) -> dict:
    """Helper para convertir documento MongoDB a dict"""
    return {
        "id": str(review["_id"]),
        "nombre_establecimiento": review["nombre_establecimiento"],
        "direccion_postal": review["direccion_postal"],
        "coordenadas": review["coordenadas"],
        "valoracion": review["valoracion"],
        "email_autor": review["email_autor"],
        "nombre_autor": review["nombre_autor"],
        "fecha_emision": review["fecha_emision"],
        "fecha_caducidad": review["fecha_caducidad"],
        "token_oauth": review["token_oauth"],
        "imagenes": review.get("imagenes", []),
        "created_at": review["created_at"]
    }


@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(current_user: UserBase = Depends(get_current_user)):
    """Obtener todas las reseñas"""
    reviews = []
    async for review in reviews_collection.find():
        reviews.append(review_helper(review))
    return reviews


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: str, current_user: UserBase = Depends(get_current_user)):
    """Obtener detalle de una reseña específica"""
    try:
        review = await reviews_collection.find_one({"_id": ObjectId(review_id)})
    except:
        raise HTTPException(status_code=400, detail="ID de reseña inválido")
    
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
    
    return review_helper(review)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    current_user: UserBase = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Crear una nueva reseña"""
    # Decodificar token para obtener información
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("email", current_user.email)
        nombre = payload.get("name", current_user.username)
        fecha_emision = datetime.fromtimestamp(payload.get("iat", datetime.now().timestamp()))
        fecha_caducidad = datetime.fromtimestamp(payload.get("exp", datetime.now().timestamp()))
    except:
        raise HTTPException(status_code=400, detail="Error al decodificar token")
    
    # Crear documento de reseña
    review_doc = {
        "nombre_establecimiento": review.nombre_establecimiento,
        "direccion_postal": review.direccion_postal,
        "coordenadas": {
            "lon": review.coordenadas.lon,
            "lat": review.coordenadas.lat
        },
        "valoracion": review.valoracion,
        "email_autor": email,
        "nombre_autor": nombre,
        "fecha_emision": fecha_emision,
        "fecha_caducidad": fecha_caducidad,
        "token_oauth": token,
        "imagenes": review.imagenes if review.imagenes else [],
        "created_at": datetime.now()
    }
    
    result = await reviews_collection.insert_one(review_doc)
    review_doc["_id"] = result.inserted_id
    
    return review_helper(review_doc)
