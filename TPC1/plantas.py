import json

f = open("plantas.json")
bd = json.load(f)
f.close()

ttl = ""

# planta é um dicionario
for planta in bd:
    rua = planta["Rua"].replace('\"', '\\"')
    registo = f"""

:p_{planta["Id"]} rdf:type owl:NamedIndividual ,
                     :Planta ;
            :temRua :r_{planta["Código de rua"]} ;
            :caldeira "{planta["Caldeira"]}" ;
            :data_atualizacao "{planta["Data de actualização"]}" ;
            :data_plantacao "{planta["Data de Plantação"]}" ;
            :especie "{planta["Espécie"]}" ;
            :estado "{planta["Estado"]}" ;
            :gestor "{planta["Gestor"]}" ;
            :id "{planta["Id"]}"^^xsd:int ;
            :implantacao "{planta["Implantação"]}" ;
            :intervencoes "{planta["Número de intervenções"]}"^^xsd:int ;
            :nome_cientifico "{planta["Nome Científico"]}" ;
            :numero "{planta["Número de Registo"]}"^^xsd:int ;
            :origem "{planta["Origem"]}" ;
            :tutor "{planta["Tutor"]}" .

:r_{planta["Código de rua"]} rdf:type owl:NamedIndividual ;
           :temPlanta :p_{planta["Id"]} ;
           :codigo_rua "{planta["Código de rua"]}"^^xsd:int ;
           :freguesia "{planta["Freguesia"]}" ;
           :local "{planta["Local"]}" ;
           :nome_rua "{rua}" .
"""                                         
    ttl += registo

output_file_name = "output.ttl"

with open(output_file_name, "w") as output_file:
    output_file.write(ttl)