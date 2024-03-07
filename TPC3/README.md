# TP3 - Mapa Virtual - SPARQL
__Data:__ 02/3/2024

__Autor:__ Robert Szabo

__UC:__ RPCW

---

Este trabalho teve como objetivo a análise de um dataset sobre cidades e ligações entre elas, de forma a conseguir responder a algumas perguntas sobre o dataset. 

## Estrutura do Ficheiro JSON
O ficheiro JSON tem a seguinte estrutura:

```json
[
    {
    "cidades": [
        {
            "id": "c1",
            "nome": "Paços de Ferreira",
            "população": "400888",
            "descrição": "Occaecat labore quis et irure nulla Lorem. Exercitation excepteur tempor est ex incididunt sunt id veniam culpa reprehenderit. Qui culpa consectetur quis officia ipsum deserunt cupidatat fugiat. Aute aliquip non sit laborum cillum.",
            "distrito": "Porto"
        },
        ...
    ],
    "ligacoes": [
        {
            "id": "l42",
            "origem": "c1",
            "destino": "c89",
            "distância": 244.169
        },
        ...
    ]
    }
]
``` 

## Ontologia e povoamento 

Criou-se uma ontologia (em ttl) com estes dados, com auxilio da ferramenta _Protégé_ e uma script em _Python_ que permite o povoamento das classes a partir do ficheiro _JSON_. 

### Classes geradas
- cidade: 
    - Data properties:
        - id
        - nome
        - população
        - descrição
        - distrito
- ligacao: 
    - Data properties:
        - id
        - distancia
    - Object properties (ligacao &rarr; cidade):
        - origem
        - destino


## GraphDB
Foi criado um repositório no GraphDB, importada a ontologia _mapa-virtual.ttl_, podendo assim utilizar-se a ferrmaneta _SPARQL_ para realização das _queries_ necessárias para responder às perguntas propostas:


1. Quais as cidades de um determinado distrito?

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?nome where { 
	?s :distrito "Porto" .
    ?s :nome ?nome
}
```


2. Distribuição de cidades por distrito?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?distrito (COUNT(distinct ?cidade) as ?ncidades) where { 
    ?cidade :distrito ?distrito .
}
group by ?distrito
```

3. Quantas cidades se podem atingir a partir do Porto? (Diretamente)
```sql
    PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>

    SELECT distinct ?cidade WHERE {
        ?porto :distrito "Porto" .
        ?ligacao :origem ?porto .
        ?ligacao :destino ?c .
        ?c :nome ?cidade
    }
```


4. Quais as cidades com população acima de um determinado valor?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>

SELECT ?nome ?populacao WHERE {
    ?cidade a :cidade .
    ?cidade :nome ?nome .
    ?cidade :populacao ?populacao .
    FILTER (100000 < ?populacao).
}
```

---

