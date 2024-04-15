import json

f = open("data/aval-alunos.json")
bd = json.load(f)
f.close()

ttl = ""

# aluno é um dicionario
for aluno in bd['alunos']:
    idAluno = aluno['idAluno']
    
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/avaliacao#Aluno_{idAluno}
:Aluno_{idAluno} rdf:type owl:NamedIndividual ,
                       :Aluno ;
"""
    exames = aluno['exames']
    if 'normal' in exames:
        registo += f"              :temExame :Exame_N_{idAluno} ;\n"
    if 'recurso' in exames:
        registo += f"              :temExame :Exame_R_{idAluno} ;\n"
    if 'especial' in exames:
        registo += f"              :temExame :Exame_E_{idAluno} ;\n"

    for tpc in aluno['tpc']:
        registo += f"              :temTPC :TPC_{tpc['tp'].replace('tpc', '')}_{idAluno} ;\n"

    registo += f"""
              :curso "{aluno['curso']}" ;
              :id_aluno "{idAluno}" ;
              :nome "{aluno['nome']}" ;
              :nota_projeto {aluno['projeto']} .
"""

    if 'normal' in exames:
        registo += f"""
    :Exame_N_{idAluno} rdf:type owl:NamedIndividual ,
                         :ExameNormal ;
                :nota {exames['normal']} .
"""
    if 'recurso' in exames:
        registo += f"""
    :Exame_R_{idAluno} rdf:type owl:NamedIndividual ,
                         :ExameRecurso ;
                :nota {exames['recurso']} .
"""

    if 'especial' in exames:
        registo += f"""
    :Exame_E_{idAluno} rdf:type owl:NamedIndividual ,
                         :ExameEspecial ;
                :nota {exames['especial']} .
"""

    for tpc in aluno['tpc']:
        registo += f"""
    :TPC_{tpc['tp'].replace("tpc", "")}_{idAluno} rdf:type owl:NamedIndividual ,
                    :TPC ;
        :nome "{tpc['tp']}" ;
        :nota {tpc['nota']} .
"""                                         
    
    ttl += registo

# append ttl to avaliacao.ttl file but on a copy of it
f = open("data/avaliacao.ttl", "r")
f2 = open("data/avaliacao_povoado.ttl", "w")
f2.write(f.read())
f.close()
f2.write(ttl)
f2.close()
