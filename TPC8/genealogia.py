import xml.etree.ElementTree as ET

f = open("biblia.xml")
bd = ET.parse(f)
f.close()

root = bd.getroot()

people = {}
ttl = ""

for person in root.iter('person'):
    # id: sex
    people[person[0].text] = person.find('sex').text
    
for person in root.iter('person'):
    id = person[0].text
    name = person.find('namegiven').text
    
    parents = person.findall('parent')
    mae, pai = "", ""
    
    for parent in parents:
        parent_id = parent.attrib['ref']
        if people[parent_id] == 'F':
            mae = parent_id
        else:
            pai = parent_id
    
    register = f"""
###  http://rpcw.di.uminho.pt/2024/familia#{id}
    :{id} rdf:type owl:NamedIndividual ,
                 :Pessoa ;
           :nome "{name}" .
"""
    if pai != "":
        register += f"    :{id} :temPai :{pai} .\n"
    if mae != "":
        register += f"    :{id} :temMae :{mae} .\n"
    
    
    ttl += register
            
f = open("familia.ttl", "a")
f.write(ttl)
f.close()