from pydantic import BaseModel, Field
from typing import Optional, List

class ProductQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Texto de busca do produto")

class ProductSuggestion(BaseModel):
    ncm: str = Field(..., description="Código NCM do produto")
    description: str = Field(..., description="Descrição do produto")
    attributes: Optional[List[str]] = Field(default=None, description="Lista de atributos do produto")

class ProductResponse(BaseModel):
    suggestions: List[ProductSuggestion]
    
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Mensagem de erro")

class HealthCheck(BaseModel):
    status: str = Field(..., description="Status da API")
