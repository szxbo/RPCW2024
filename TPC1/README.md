# Análise de Ficheiro JSON e Conversão para Protegé
Este repositório contém um script em Python que analisa um ficheiro JSON com informações sobre plantas, e converte esses dados em código Turtle (TTL) para ser utilizado no Protegé.

# Estrutura do Ficheiro JSON
O ficheiro JSON tem a seguinte estrutura:

```json
[
  {
    "Id": 20615557,
    "Número de Registo": 3,
    "Código de rua": 1685467,
    "Rua": "Rua Júlio Dinis",
    "Local": "Zambujeiro",
    "Freguesia": "Alcabideche",
    "Espécie": "pinheiro manso",
    "Nome Científico": "Pinus pinea",
    "Origem": "",
    "Data de Plantação": "",
    "Estado": "Adulto",
    "Caldeira": "Sim",
    "Tutor": "Sim",
    "Implantação": "Arruamento",
    "Gestor": "DGEV",
    "Data de atualização": "23/07/2021 19:50:54",
    "Número de intervenções": 6
  },
  // Outros objetos...
]
``` 
# Classes Geradas
- Planta: Contém a maioria das informações sobre as plantas.
- Rua: Contém informações específicas sobre a rua (Rua, Código de Rua, Local e Freguesia).

Para os atributos destas classes 

# Exemplo de Código TTL Gerado
```turtle
:p_20615557 rdf:type owl:NamedIndividual ,
                     :Planta ;
            :temRua :r_1685467 ;
            :caldeira "Sim" ;
            :data_atualizacao "23/07/2021 19:50:54" ;
            :data_plantacao "" ;
            :especie "pinheiro manso" ;
            :estado "Adulto" ;
            :gestor "DGEV" ;
            :id "20615557"^^xsd:int ;
            :implantacao "Arruamento" ;
            :intervencoes "6"^^xsd:int ;
            :nome_cientifico "Pinus pinea" ;
            :numero "3"^^xsd:int ;
            :origem "" ;
            :tutor "Sim" .

:r_1685467 rdf:type owl:NamedIndividual ;
           :temPlanta :p_20615557 ;
           :codigo_rua "1685467"^^xsd:int ;
           :freguesia "Alcabideche" ;
           :local "Zambujeiro" ;
           :nome_rua "Rua Júlio Dinis" .
```
