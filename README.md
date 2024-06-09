# Projeto Pokédex

## Visão Geral

Este projeto consiste em um sistema de Pokédex desenvolvido com um backend em FastAPI e um frontend em Angular. A Pokédex permite pesquisar Pokémon e visualizar detalhes específicos.

## Backend

### Tecnologias Utilizadas

- **FastAPI**: Framework web para construir APIs rápidas com Python.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.

### Endpoints Principais

- `GET /pokemons`: Retorna uma lista paginada de Pokémon.
- `GET /pokemons/{id}`: Retorna os detalhes de um Pokémon pelo ID.
- `GET /export_pokemons`: Exporta a lista de Pokémon para um arquivo XML.
- `GET /docs`: Acesso à documentação Swagger gerada automaticamente.
- `GET /redoc`: Acesso à documentação ReDoc gerada automaticamente.

### Instalação e Execução

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/juniortro/pokedex
    ```
2. **Rodando o backend:** <br>
    Na primeira vez ele irá rodar um script que busca todos os Pokémons e popula uma base em PostgreSQL, portanto
    pode demorar uns segundos para subir.
    ```bash
    docker-compose up --build
    ```
3. **Rodando o frontend:** <br>
    ```bash
    npm install
    ng serve
    ```
