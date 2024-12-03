from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .models import ProductQuery, ProductSuggestion
from typing import List
import openai

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cmexfront-git-main-williams-projects-2c392421.vercel.app",
        "https://localhost:5173",
        "https://cmexfront.vercel.app",
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura a chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/sugg", response_model=List[ProductSuggestion])
async def get_suggestions(product_query: ProductQuery):
    try:
        if len(product_query.query.strip()) < 3:
            return []

        prompt = f"""
        Analise o seguinte produto e forneça:
        1. O código NCM mais apropriado
        2. Uma breve descrição do produto
        3. Principais atributos

        Produto: {product_query.query}

        Responda em formato estruturado, separando NCM e descrição.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ou o modelo de sua preferência
            messages=[
                {"role": "system", "content": "Você é um especialista em classificação NCM de produtos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        # Processa a resposta da API
        content = response.choices[0].message.content

        # Exemplo simplificado de parsing da resposta
        lines = content.strip().split('\n')
        ncm = lines[0] if len(lines) > 0 else ""
        description = lines[1] if len(lines) > 1 else ""

        suggestions = [
            ProductSuggestion(
                ncm=ncm,
                description=description
            )
        ]

        return suggestions

    except Exception as e:
        print(f"Erro ao obter sugestões: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar a solicitação.")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}