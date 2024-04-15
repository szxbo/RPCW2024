# TP8  - Familia
__Data:__ 15/4/2024

__Autor:__ Robert Szabo

__UC:__ RPCW

---

O objetivo deste TPC é usar a ontologia dada sobre famílias, que contém poucas informações como o nome de uma `Pessoa` e as object properties `temPai` e `temMae`.

O desafio colocado consiste em, a partir de um ficheiro XML com informação sobre famílias, criar um script em Python que adicione essa informação à ontologia.

Das duas opções `biblia.xml` e `royal.xml` foi escolhido o ficheiro `biblia.xml` que contém informação sobre a genealogia de algumas personagens bíblicas.

A leitura do ficheiro XML é feita com a biblioteca `xml.etree.ElementTree` e a adição de informação à ontologia é feita concatenando strings diretamente ao ficheiro `familia.ttl`.

O script foi testado com sucesso e a ontologia foi carregada no Protegé.

---

Exemplo da informação sobre uma pessoa no ficheiro `biblia.xml`:
```xml
<person>
	<id>I1</id>
	<name>Mizraim //</name>
	<namegiven>Mizraim</namegiven>
	<sex>M</sex>
	<uid>A0249835B2ABD6118B8E0004760DB7A0CC1E</uid>
	<familyasspouse ref="F1">F1</familyasspouse>
	<familyaschild ref="F2">F2</familyaschild>
	<parent ref="I34">Ham</parent>
	<parent ref="I7">Egyptus</parent>
	<child ref="I96">Ludim</child>
	<child ref="I97">Anamim</child>
	<child ref="I98">Lehabim</child>
	<child ref="I99">Nephtuihim</child>
	<child ref="I100">Pethusim</child>
	<child ref="I101">Caphtorim</child>
	<child ref="I102">Casluhim</child>
</person>
```

Exemplo da informação sobre uma família gerada pelo script:
```turtle
###  http://rpcw.di.uminho.pt/2024/familia#I1
    :I1 rdf:type owl:NamedIndividual ,
                 :Pessoa ;
           :nome "Mizraim" .
    :I1 :temPai :I34 .
    :I1 :temMae :I7 .


###  http://rpcw.di.uminho.pt/2024/familia#I7
    :I7 rdf:type owl:NamedIndividual ,
                 :Pessoa ;
           :nome "Egyptus" .

###  http://rpcw.di.uminho.pt/2024/familia#I34
    :I34 rdf:type owl:NamedIndividual ,
                 :Pessoa ;
           :nome "Ham" .
    :I34 :temPai :I23 .
    :I34 :temMae :I35 .    
```

---