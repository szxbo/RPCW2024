import json

dataset = open("mapa-virtual.json")
bd = json.load(dataset)
dataset.close()


individuals_ttl = ""
for cidade in bd["cidades"]:
    individuals_ttl+=f"""
    
###  http://rpcw.di.uminho.pt/2024/mapa-virtual#{cidade["id"]}
:{cidade["id"]} rdf:type owl:NamedIndividual ,
             :cidade ;
    :descricao "{cidade["descrição"]}" ;
    :distrito "{cidade["distrito"]}" ;
    :id "{cidade["id"]}" ;
    :nome "{cidade["nome"]}" ;
    :populacao {cidade["população"]} .
    """
    
for ligacao in bd["ligacoes"]:
    individuals_ttl+=f"""
    
###  http://rpcw.di.uminho.pt/2024/mapa-virtual#{ligacao["id"]}
:{ligacao["id"]} rdf:type owl:NamedIndividual ,
             :ligacao ;
    :destino :{ligacao["destino"]} ;
    :origem :{ligacao["origem"]} ;
    :distancia {ligacao["distância"]} ;
    :id "{ligacao["id"]}" .
"""

mapa_virtual = open("mapa-virtual.ttl", 'a')
mapa_virtual.write(individuals_ttl)
mapa_virtual.close()