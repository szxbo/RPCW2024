# TPC5 - Dataset de Filmes
__Data:__ 14/3/2024

__Autor:__ Robert Szabo

__UC:__ RPCW

Este script é usado para consultar uma base de dados de filmes. Com o uso de queries SPARQL, é possível fazer uma data de perguntas sobre os filmes, como por exemplo, listar todos os filmes, listar os filmes de um determinado género, listar os filmes de um determinado ator, listar os filmes de um determinado diretor, entre outros.

## Detalhes da Consulta
O script busca os seguintes detalhes sobre cada filme:
- URI
- Nome do Filme
- Duração
- País
- Nome do Diretor
- Nome do Produtor
- Nome do Ator
- Nome do Compositor
- Nome do Escritor
- Descrição

Com o uso de blocos opcionais é possível lidar com casos em que certas informações podem não estar disponíveis para um filme. Por exemplo, nem todos os filmes podem ter uma duração conhecida ou um compositor conhecido. Nestes casos, o script ainda retornará os outros detalhes do filme.

Este também está pronto para lidar com casos em que um filme pode ter mais de um diretor, produtor, ator, compositor ou escritor.

## Filtragem de Idioma
São filtrados os resultados para incluir apenas filmes cujos detalhes estão disponíveis em inglês. Isso é feito usando a função filter(lang(?variable) = 'en') no SPARQL.

## Ficheiro JSON gerado
O script gera um ficheiro JSON com os detalhes de cada filme. O ficheiro tem a seguinte estrutura:

```json
[
    {
        "movie": "Cactus Flower (film)",
        "description": [
            "Cactus Flower is a 1969 American screwball comedy film directed by Gene Saks and starring Walter Matthau, Ingrid Bergman, and Goldie Hawn..."
        ],
        "genre": [
            "Film score"
        ],
        "country": [
            "United States"
        ],
        "directors": [
            "Gene Saks"
        ],
        "actors": [
            "Ingrid Bergman",
            "Goldie Hawn",
            "Walter Matthau"
        ],
        "producers": [],
        "writers": [],
        "composers": [
            "Quincy Jones"
        ],
        "duration": 103.0
    }
]