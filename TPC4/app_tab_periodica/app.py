from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%d / %H:%M:%S')

# GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/tab_periodica"

@app.route('/')
def index():
    return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/elementos')
def elementos():
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?name ?symb ?na ?group_num ?group_name where {
        ?s a tp:Element ;
           tp:name ?name ;
           tp:symbol ?symb ;
           tp:atomicNumber ?na .
        ?s tp:group ?group .
        optional {?group tp:number ?group_num .}
        optional {?group tp:name ?group_name.}
    }
    order by ?na 
    """
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        # correu tudo bem    
        dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
        return render_template('elementos.html', data = dados, time = data_iso_formatada)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})

    
@app.route('/grupos')
def grupos():
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?group_num ?group_name where {
		?s a tp:Group .
    	optional { ?s tp:number ?group_num .}
	    optional { ?s tp:name ?group_name .}
    }
    order by ?group_num
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        # correu tudo bem    
        dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
        return render_template('grupos.html', data = dados, time = data_iso_formatada)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})
    


@app.route('/grupo/<int:group_num>')
def grupo_num(group_num):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT ?na ?symb ?name WHERE{{
    ?s rdf:type tp:Element;
    	tp:name ?name;
    	tp:atomicNumber ?na;
    	tp:symbol ?symb.
    ?s tp:group ?g.
    ?g rdf:type tp:Group;
    	tp:number "{group_num}"^^xsd:integer .
    }}
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        # correu tudo bem    
        dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
        return render_template('grupo.html', data = dados, group_id=group_num, time = data_iso_formatada)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/grupo/<string:group_name>')
def grupo_nome(group_name):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT ?na ?symb ?name WHERE{{
    ?s rdf:type tp:Element;
    	tp:name ?name;
    	tp:atomicNumber ?na;
    	tp:symbol ?symb.
    ?s tp:group ?g.
    ?g rdf:type tp:Group;
    	tp:name "{group_name}" .
    }}
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        # correu tudo bem    
        dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
        return render_template('grupo.html', data = dados, group_id=group_name, time = data_iso_formatada)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/elementos/<elem>')
def elemento(elem):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    SELECT ?name ?symb ?an ?aw ?color ?group_num ?group_name ?period_num WHERE{{
    ?s  tp:name "{elem}" ;
    	tp:symbol ?symb ;
        tp:atomicNumber ?an ;
    	tp:atomicWeight ?aw ;
    	tp:color ?color ;
        tp:group ?group ;
    	tp:period ?period .
    optional {{?group tp:num ?group_num .}}
    optional {{?group tp:name ?group_name .}}
    ?period tp:number ?period_num .
    }}
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        # correu tudo bem    
        dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
        return render_template('elemento.html', data = dados, elem_name = elem, time = data_iso_formatada)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})

if __name__ == "__main__":
    app.run(debug=True)