## Bot Microempreendedor Individual
Um bot que raspa dados da base de MEIs da Receita Federal

### Atenção

Rodando apenas com [Firefox browser](https://www.mozilla.org/en-US/firefox/new/)

### Pré-requisitos

Instale [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)

Instale [selenium](https://selenium-python.readthedocs.io/installation.html)

### Exemplos
*Abra o console python*

Extraindo todas UFs por município e CNAE (e armazenando na pasta 'files'):

```python
>>> import bot
>>> bot.ufs_por_municipio_e_cnae('files')
```
Uma UF específica:
```python
>>> bot.uf_por_municipio_e_cnae('files', uf='PARÁ')
```

Dê uma olhada na [lista de ufs](https://github.com/bernarducs/mei/blob/master/lista%20de%20uf.txt) 
