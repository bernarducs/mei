## Bot Microempreendedor Individual
Um bot que raspa dados da base de MEIs da Receita Federal

### Relatórios implementados

* MEIs por Municípios e CNAE (um arquivo por UF)
* MEIs por sexo e CNAE (um arquivo por UF)

### Atenção

Rodando apenas com [Firefox browser](https://www.mozilla.org/en-US/firefox/new/)

### Pré-requisitos

Instale [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)

Instale [selenium](https://selenium-python.readthedocs.io/installation.html)

### Exemplos
*Abra o console python*

Extraindo todas UFs por município e CNAE (e armazenando na pasta 'arquivos'):

```python
>>> import bot
>>> bot.ufs_por_municipio_e_cnae('arquivos')
```
Uma UF específica:
```python
>>> bot.uf_por_municipio_e_cnae('arquivos', uf='PARÁ')
```
Todas as UF por sexo e cnae:
```python
>>> bot.ufs_por_sexo_cnae('arquivos')
```
Rodando o comando anterior sem o modo headless:
```python
>>> bot.ufs_por_sexo_cnae('arquivos', headless=False)
```

Dê uma olhada na [lista de ufs](https://github.com/bernarducs/mei/blob/master/lista%20de%20uf.txt) 
