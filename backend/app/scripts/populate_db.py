import asyncio
import httpx
from sqlalchemy import inspect

from ..database.database import SessionLocal, engine
from ..models.models import Pokemon, Base

def create_tables_if_not_exists():
    inspector = inspect(engine)
    if not inspector.has_table('pokemon'):
        Base.metadata.create_all(bind=engine)

def is_database_populated(db):
    return db.query(Pokemon).first() is not None

async def populate_db():
    db = SessionLocal()
    if not is_database_populated(db):
        pokemons_from_api = await get_all_pokemons_from_api()
        for pokemon_data in pokemons_from_api:
            name = pokemon_data["name"]
            db_pokemon = Pokemon(name=name)
            db.add(db_pokemon)
    
        db.commit()
        print("Banco de dados populado com sucesso!")
    else:
        print("O banco de dados já está populado. Nenhuma ação foi realizada.")
    db.close()

async def get_all_pokemons_from_api():
    base_api_url = "https://pokeapi.co/api/v2/pokemon"
    try:
        all_pokemons = []
        offset = 0
        limit = 20 

        while True:
            api_url = f"{base_api_url}?offset={offset}&limit={limit}"
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url)
                if response.status_code == 200:
                    pokemon_data = response.json()["results"]
                    all_pokemons.extend(pokemon_data)
                
                    if len(pokemon_data) < limit:
                        break
                
                    offset += limit
                else:
                    print(f"Erro ao fazer requisição à API: {response.status_code}")
                    return None
        return all_pokemons
    except Exception as e:
        print(f"Erro ao fazer requisição à API: {str(e)}")
        return None

if __name__ == "__main__":
    create_tables_if_not_exists()
    asyncio.run(populate_db())
