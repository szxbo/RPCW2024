import json

f = open("musica.json")
bd = json.load(f)
f.close()


ttl = ""
for instrumento in bd["instrumentos"]:
    instrumento["#text"] = instrumento["#text"].replace(" ", "_")
    ttl+=f"""

###  http://rpcw.di.uminho.pt/2024/musica#{instrumento["#text"]}
:{instrumento["#text"]} rdf:type owl:NamedIndividual ;
            :idinstrumento "{instrumento["id"]}" ;
           :instrumento "{instrumento["#text"]}" .
    """
    
for curso in bd["cursos"]:
    curso["instrumento"]["#text"] = curso["instrumento"]["#text"].replace(" ", "_")
    curso["designacao"] = curso["designacao"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ;
     :ensinaIntrumento :{curso["instrumento"]["#text"]} ;
     :designacao "{curso["designacao"]}" ;
     :duracao {curso["duracao"]} ;
     :idCurso "{curso["id"]}" .


"""
  
    
for aluno in bd["alunos"]:
    aluno["nome"]=aluno["nome"].replace(" ", "_")
    aluno["instrumento"] = aluno["instrumento"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ;
        :temCurso :{aluno["curso"]} ;
        :temInstrumento :{aluno["instrumento"]} ;
        :anoCurso {aluno["anoCurso"]} ;
        :dataNasc "{aluno["dataNasc"]}" ;
        :idAluno "{aluno["id"]}" ;
        :nome "{aluno["nome"]}" ."""

with open("output.ttl", "w") as output_file:
    output_file.write(ttl)