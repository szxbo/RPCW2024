from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%d / %H:%M:%S')


# GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/Alunos"

def process_results(api_get, results):
    alunos = []
    for result in results:
        if api_get == 'alunos':
            aluno = {}
            aluno['id'] = result['id']['value']
            aluno['nome'] = result['nome']['value']
            aluno['curso'] = result['curso']['value']
            alunos.append(aluno)
            
        if api_get == 'alunos_id':
            # check if aluno already exists
            if alunos != []:
                aluno = alunos[0]
                aluno['tpcs'][result['num_tpc']['value']] = result['nota_tpc']['value']
                exame_tipo = result['exames']['value'].split('/')[-1].split('_')[1]
                if exame_tipo == 'N':
                    aluno['exames']['normal'] = result['nota_exame']['value']
                elif exame_tipo == 'R':
                    aluno['exames']['recurso'] = result['nota_exame']['value']
                elif exame_tipo == 'E':
                    aluno['exames']['especial'] = result['nota_exame']['value']
            else:
                aluno = {}
                aluno['id'] = result['id']['value']
                aluno['nome'] = result['nome']['value']
                aluno['curso'] = result['curso']['value']
                aluno['nota_projeto'] = result['nota_projeto']['value']
                aluno['tpcs'] = {result['num_tpc']['value']: result['nota_tpc']['value']}
                exame_tipo = result['exames']['value'].split('/')[-1].split('_')[1]
                if exame_tipo == 'N':
                    aluno['exames'] = {'normal': result['nota_exame']['value']}
                elif exame_tipo == 'R':
                    aluno['exames'] = {'recurso': result['nota_exame']['value']}
                elif exame_tipo == 'E':
                    aluno['exames'] = {'especial': result['nota_exame']['value']}
                alunos.append(aluno)
            
        if api_get == 'alunos_curso':
            aluno = {}
            aluno['id'] = result['id']['value']
            aluno['nome'] = result['nome']['value']
            alunos.append(aluno)
            
        if api_get == 'tpc':
            aluno = {}
            aluno['id'] = result['id']['value']
            aluno['nome'] = result['nome']['value']
            aluno['curso'] = result['curso']['value']
            aluno['num_tpcs'] = result['num_tpcs']['value']
            alunos.append(aluno)
            
        if api_get == 'curso':
            curso = {}
            curso[result['curso']['value']] = result['num_alunos']['value']
            alunos.append(curso)
            
        if api_get == 'projeto':
            nota_projeto = {}
            nota_projeto[result['nota_proj']['value']] = result['num_alunos']['value']
            alunos.append(nota_projeto)
            
        if api_get == 'recurso':
            aluno = {}
            aluno['id'] = result['id']['value']
            aluno['nome'] = result['nome']['value']
            aluno['curso'] = result['curso']['value']
            aluno['nota_recurso'] = result['nota_exame']['value']
            alunos.append(aluno)

    return alunos

def avaliacao_final(geral, tpcs):
    # criar um dicionário com os tpcs
    tpcs = {tpc['id']['value']: tpc['total']['value'] for tpc in tpcs}
    alunos = []
    for a in geral:
        aluno = {}
        aluno['id'] = a['id']['value']
        aluno['nome'] = a['nome']['value']
        aluno['curso'] = a['curso']['value']
        if int(a['nota_proj']['value']) < 10:
            aluno['avaliacao_final'] = 'R'
        elif int(a['max_exames']['value']) < 10:
            aluno['avaliacao_final'] = 'R'
        else:
            aluno['avaliacao_final'] = "{:.2f}".format((int(a['nota_proj']['value'])*0.4 + int(a['max_exames']['value'])*0.4 + float(tpcs[a['id']['value']])))
        alunos.append(aluno)
    return alunos

@app.route('/')
def index():
    return render_template('index.html', data = {"data": data_iso_formatada})

"""
GET /api/alunos
GET /api/alunos/:id
GET /api/alunos?curso=X 
GET /api/alunos/tpc
GET /api/alunos?groupBy=curso
GET /api/alunos?groupBy=projeto
GET /api/alunos?groupBy=recurso
GET /api/alunos/avaliados
"""

@app.route('/api/alunos')
def alunos():
    if 'curso' in request.args:
        curso = request.args['curso']
        sparql_query = f"""
        PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?id ?nome where {{
            ?s rdf:type a:Aluno ;
               a:id_aluno ?id ;
               a:nome ?nome ;
               a:curso ?curso .
            FILTER(?curso = "{curso}")
        }}
        ORDER BY (?nome)
        """
        resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})

        if resposta.status_code == 200:
            dados = resposta.json()['results']['bindings']
            return process_results('alunos_curso', dados)
        else:
            return render_template('index.html', data = {"data": data_iso_formatada})
    elif 'groupBy' in request.args:
        groupBy = request.args['groupBy']
        if groupBy == 'curso':
            sparql_query = """
            PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select ?curso (COUNT(DISTINCT ?s) as ?num_alunos) where {
                ?s rdf:type a:Aluno ;
                   a:curso ?curso .
            }

            GROUP BY ?curso
            """
            resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
            if resposta.status_code == 200:
                dados = resposta.json()['results']['bindings']
                return process_results('curso', dados)
            else:
                return render_template('index.html', data = {"data": data_iso_formatada})   
        elif groupBy == 'projeto':
            sparql_query = """
            PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select ?nota_proj (COUNT(DISTINCT ?s) as ?num_alunos) where {
                ?s rdf:type a:Aluno ;
                   a:nota_projeto ?nota_proj .
            }

            GROUP BY ?nota_proj
            ORDER BY ASC (?nota_proj)
            """
            resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
            if resposta.status_code == 200:
                dados = resposta.json()['results']['bindings']
                return process_results('projeto', dados)
            else:
                return render_template('index.html', data = {"data": data_iso_formatada})
        elif groupBy == 'recurso':
            sparql_query = """
            PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            select ?id ?nome ?curso ?nota_exame where {
                ?s rdf:type a:Aluno ;
                   a:id_aluno ?id ;
                   a:nome ?nome ;
                   a:curso ?curso ;
                   a:temExame ?exame .

                ?exame rdf:type a:ExameRecurso .
                ?exame a:nota ?nota_exame.
            }

            ORDER BY ?nome
            """
            resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
            if resposta.status_code == 200:
                dados = resposta.json()['results']['bindings']
                return process_results('recurso', dados)
            else:
                return render_template('index.html', data = {"data": data_iso_formatada})
    else:
        sparql_query = f"""
        PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?id ?nome ?curso where {{
            ?s rdf:type a:Aluno ;
               a:id_aluno ?id ;
               a:nome ?nome ;
               a:curso ?curso .
        }}

        ORDER BY (?nome)
        """
        resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})

        if resposta.status_code == 200:
            dados = resposta.json()['results']['bindings'] # experimentar fazer prints parciais à estrutura de dados
            return process_results('alunos', dados)
        else:
            return render_template('index.html', data = {"data": data_iso_formatada})
 
@app.route('/api/alunos/:<string:id>')
def alunos_id(id):
    sparql_query = f"""
    PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select ?id ?nome ?curso ?nota_projeto ?exames ?nota_exame ?num_tpc ?nota_tpc where {{
        ?s rdf:type a:Aluno ;
           a:id_aluno ?id ;
           a:nome ?nome ;
           a:curso ?curso ;
           a:nota_projeto ?nota_projeto ;
           a:temTPC ?tpcs ;
           a:temExame ?exames .

        ?exames a:nota ?nota_exame .

        ?tpcs a:nota ?nota_tpc ;
              a:nome ?num_tpc .

        FILTER(?id = "{id}")
}}
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        print(dados)
        return process_results('alunos_id', dados)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})
    
@app.route('/api/alunos/tpc')
def tpc():
    sparql_query = """
    PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select ?id ?nome ?curso (COUNT(?tpc) as ?num_tpcs) where {
        ?s rdf:type a:Aluno ;
           a:id_aluno ?id ;
           a:nome ?nome ;
           a:curso ?curso ;
           a:temTPC ?tpc .
    }
    GROUP BY ?id ?nome ?curso

    ORDER BY ?nome
    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return process_results('tpc', dados)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})
    
def recurso():
    sparql_query = """

    """
    
    resposta = requests.get(graphdb_endpoint, params = {"query": sparql_query}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})
    
@app.route('/api/alunos/avaliados')
def avaliados():
    sparql_query_geral = """
    PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select ?id ?nome ?curso ?nota_proj (MAX(?notas_exames) as ?max_exames)where {
        ?s rdf:type a:Aluno ;
           a:id_aluno ?id ;
           a:nome ?nome ;
           a:curso ?curso ;
           a:nota_projeto ?nota_proj ;

		   a:temExame ?exame .
    ?exame a:nota ?notas_exames . 
    }
    GROUP BY ?id ?nome ?curso ?nota_proj 

    ORDER BY ?nome
    """
    
    sparql_query_tpcs = """
    PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao/>
    PREFIX a: <http://rpcw.di.uminho.pt/2024/avaliacao/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select ?id (SUM(?nota_tpc) as ?total) where {
        ?s rdf:type a:Aluno ;
           a:id_aluno ?id ;
           a:temTPC ?tpc .
    	?tpc a:nota ?nota_tpc .
    }
    GROUP BY ?id 

    """
    
    resposta_geral = requests.get(graphdb_endpoint, params = {"query": sparql_query_geral}, headers= {"Accept": "application/sparql-results+json"})
    resposta_tpcs = requests.get(graphdb_endpoint, params = {"query": sparql_query_tpcs}, headers= {"Accept": "application/sparql-results+json"})
    
    if resposta_geral.status_code == 200 and resposta_tpcs.status_code == 200:
        dados_gerais = resposta_geral.json()['results']['bindings']
        dados_tpcs = resposta_tpcs.json()['results']['bindings']
        return avaliacao_final(dados_gerais, dados_tpcs)
    else:
        return render_template('index.html', data = {"data": data_iso_formatada})


if __name__ == "__main__":
    app.run(debug=True)