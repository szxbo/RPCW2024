import json
import requests

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query_template = """
    PREFIX schema: <http://schema.org/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select distinct ?uri ?movieName ?genre ?runtime ?country ?directorName ?producerName ?actorName ?composerName ?writerName ?description where {{
    ?uri a dbo:Film ;
        rdfs:label ?movieName .

    filter(lang(?movieName) = 'en')        
            
    optional {{
        ?uri dbo:runtime ?runtime .
    }}      
    optional {{
        ?uri dbo:director ?director .
        ?director dbp:name ?directorName .
        filter(lang(?directorName) = 'en')
    }}        
    optional {{ 
        ?uri dbo:starring ?cast . 
        ?cast dbp:name ?actorName .
        filter(lang(?actorName) = 'en')
    }}
    optional {{ 
        ?uri dbp:producer ?producer .
        ?producer dbp:name ?producerName .
        filter(lang(?producerName) = 'en')
    }}
    optional {{ 
        ?uri dbp:country ?country . 
        filter(lang(?country) = 'en')
    }}
    optional {{ 
        ?uri dbp:music ?composer .
        ?composer dbp:name ?composerName .
    }}
    
    optional {{
        ?uri dbo:writer ?writer.
        ?writer rdfs:label ?writerName.
        filter(lang(?writer) = 'en').
    }}

    optional {{
        ?uri rdfs:comment ?description .
        filter(lang(?description) = 'en')
    }} 
    
    optional {{
        ?uri dbp:genre  ?genreURI.
        ?genreURI rdfs:label ?genre
        filter(lang(?genre) = 'en').
    }}
}}
LIMIT {}
OFFSET {}
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

results_limit = 10000  # Define o número máximo de resultados por solicitação
offset = 0
all_results = []
counter = 0

while True:
    sparql_query = sparql_query_template.format(results_limit, offset)

    params = {
        "query": sparql_query,
        "format": "json"
    }

    response = requests.get(sparql_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        results = response.json()
        if not results["results"]["bindings"]:
            break  # Se não houver mais resultados, pare o loop
        all_results.extend(results["results"]["bindings"])
        offset += results_limit
        counter += 1
        print(counter, flush=True)
    elif response.status_code == 206:
        print("Done - no more entries")
        break
    else:
        print("Error: ", response.status_code)
       # print(response.text)
        break



movies = {}

for result in all_results:
    uri = result["uri"]["value"]
    name = result["movieName"]["value"]
    description = result.get("description", {}).get("value", None)
    duration = result.get("runtime", {}).get("value", None)
    country = result.get("country", {}).get("value", None)
    genre = result.get("genre", {}).get("value", None)
    actor = result.get("actorName", {}).get("value", None)
    director = result.get("directorName", {}).get("value", None)
    producer = result.get("producerName", {}).get("value", None)
    composer = result.get("composerName", {}).get("value", None)
    writer = result.get("writerName", {}).get("value", None)
    if uri in movies:
        if genre and genre not in movies[uri]["genre"]:
            movies[uri]["genre"].append(genre)
        if country and country not in movies[uri]["country"]:
            movies[uri]["country"].append(country)
        if actor and actor not in movies[uri]["actors"]:
            movies[uri]['actors'].append(actor)
        if director and director not in movies[uri]["directors"]:
            movies[uri]["directors"].append(director)
        if writer and writer not in movies[uri]["writers"]:
            movies[uri]["writers"].append(writer)
        if composer and composer not in movies[uri]["composers"]:
            movies[uri]["composers"].append(composer)
        if description and description not in movies[uri]["description"]:
            movies[uri]["description"].append(description)
        if producer and producer not in movies[uri]["producers"]:
            movies[uri]["producers"].append(producer)
    else:
        movies[uri] = {
            "movie": name,
            "description": [description] if description else [],
            "genre": [genre] if genre else [],
            "country": [country] if country else [],
            "directors": [director] if director else [],
            "actors": [actor] if actor else [],
            "producers": [producer] if producer else [],
            "writers": [writer] if writer else [],
            "composers": [composer] if composer else [],
        }
        if duration: movies[uri]["duration"] = float(duration)/60

        
movies_list = list(movies.values())
f = open('movies.json', 'w')
json.dump(movies_list, f)
f.close()
