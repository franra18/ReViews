from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    lon: float
    lat: float


class ReviewBase(BaseModel):
    nombre_establecimiento: str
    direccion_postal: str
    coordenadas: Location
    valoracion: int = Field(..., ge=0, le=5)


class ReviewCreate(ReviewBase):
    imagenes: Optional[list[str]] = []


class ReviewResponse(ReviewBase):
    id: str
    email_autor: str
    nombre_autor: str
    fecha_emision: datetime
    fecha_caducidad: datetime
    token_oauth: str
    imagenes: Optional[list[str]] = []
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
