## Bot Microempreendedor Individual
Um bot que raspa dados da base de MEIs da Receita Federal

### Atenção

Rodando apenas com [Firefox browser](https://www.mozilla.org/en-US/firefox/new/)

### Pré-requisitos

Instale [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)

Instale [selenium](https://selenium-python.readthedocs.io/installation.html)

### Exemplo
As linhas abaixo pega um arquivo a cada 4 horas de uma UF contendo o total de Meis por município e por CNAE.

```python
>>> from meibot import MeiBot
>>> mei = MeiBot(uf='PARÁ', delay_hours=4)
>>> while True:
>>>     mei.get_cnae_municipio_data()
```

Dê uma olhada na [lista de ufs](https://github.com/bernarducs/mei/blob/master/lista%20de%20uf.txt) for uf name list
