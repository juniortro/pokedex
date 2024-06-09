from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import List
from sqlalchemy.orm import Session
from ..database.database import get_db, Pokemon
from ..models import models
from fastapi.responses import Response
import xml.etree.ElementTree as ET

router = APIRouter()

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

@router.get("/pokemon", response_model=List[dict])
async def get_pokemons(offset: int = 0, limit: int = 20, search: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Pokemon)
    query = query.filter(models.Pokemon.name.notilike('%-%'))  # Filtra nomes que não contenham traço pois na pokeAPI não tem informação sobre os pokemons -mega
    if search:
        query = query.filter(models.Pokemon.name.ilike(f'%{search}%'))
    pokemons = query.order_by(models.Pokemon.name).offset(offset).limit(limit).all()
    return [{"id": pokemon.id, "name": pokemon.name } for pokemon in pokemons]


@router.get("/pokemon/{pokemon_id}", response_model=dict)
async def get_pokemon_details(pokemon_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{BASE_URL}/{pokemon_id}')
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from PokeAPI")
        pokemon_details = response.json()
        pokemon_info = {
            "height": pokemon_details["height"],
            "weight": pokemon_details["weight"],
            "types": pokemon_details["types"]
        }
        return pokemon_info

@router.get("/export_pokemons", response_class=Response)
async def export_pokemons_to_xml(db: Session = Depends(get_db)):
    pokemons = db.query(models.Pokemon).order_by(models.Pokemon.name).all()

    root = ET.Element("pokemons")

    for pokemon in pokemons:
        pokemon_element = ET.SubElement(root, "pokemon")
        id_element = ET.SubElement(pokemon_element, "id")
        id_element.text = str(pokemon.id)
        name_element = ET.SubElement(pokemon_element, "name")
        name_element.text = pokemon.name

    response = ET.tostring(root, encoding="utf-8")
    return Response(content=response, media_type="application/xml")