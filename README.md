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

Extraindo todas UFs por município e CNAE (cria e armazena numa subpasta "arquivos"):

```console
python bot.py ufs_por_municipio_cnae
```

Uma UF específica:
```console
python bot.py uf_por_municipio_e_cnae --uf="PARÁ"
```
######  *Dê uma olhada na [lista de ufs](https://github.com/bernarducs/mei/blob/master/lista%20de%20uf.txt)*

Todas as UF por sexo e cnae, determinado uma pasta para donwload (windows):
```console
python bot.py uf_por_sexo_e_cnae --pasta="C\:Documents\bot_files"
```

Rodando o comando anterior sem o modo headless:
```console
python bot.py uf_por_sexo_e_cnae --headless=False
``` 