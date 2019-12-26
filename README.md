# Bot Microempreendedor Individual
a bot that scrap micro entrepreneurs subscriptions data from brazilian IRS

## Attention

Only with [Firefox browser](https://www.mozilla.org/en-US/firefox/new/)

### Prerequisites

######  Install [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)
###### Install [selenium](https://selenium-python.readthedocs.io/installation.html)

## Example

These lines grab a file every 4 hours, containing the total of MEIs per municipality per CNAE

```python
>>> from meibot import MeiBot
>>> mei = MeiBot(uf='PARÁ', delay_hours=4)
>>> mei.get_cnae_municipio_data()
```

Take a look at [lista de uf.txt](https://github.com/bernarducs/mei/blob/master/lista%20de%20uf.txt) for uf name list
