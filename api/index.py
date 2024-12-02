from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
from .models import ProductQuery, ProductSuggestion
from typing import List

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI()

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cmexfront-hnq5ruasb-williams-projects-2c392421.vercel.app"],  # Origem do frontend
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/api/index", response_model=List[ProductSuggestion])
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

        response = client.chat.completions.create(
            model="gpt-4",  # ou o modelo de sua preferência
            messages=[
                {"role": "system", "content": "Você é um especialista em classificação NCM de produtos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        # Processa a resposta da API
        content = response.choices[0].message.content
        
        # Aqui você precisaria parsear a resposta para extrair NCM e descrição
        # Este é um exemplo simplificado
        suggestions = [
            ProductSuggestion(
                ncm=content.split('\n')[0],
                description=content.split('\n')[1] if len(content.split('\n')) > 1 else ""
            )
        ]

        return suggestions

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
