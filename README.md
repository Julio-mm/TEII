# Tecnologías Específicas en Ingeniería Informática • Paquete `teii`

## Funcionalidad

El paquete `teii` consta de un único subpaquete  `teii.finance`. Este subpaquete
implementa una jerarquía de clases para realizar consultas a alguna de las
interfaces `HTTP` de [Alpha Vantage](https://www.alphavantage.co/). Estas
interfaces proporcionan información financiera de diferentes naturaleza. La
[documentación de Alpha Vantage](https://www.alphavantage.co/documentation/)
describe todas estas interfaces. Para cada una de ellas, se describen los
parámetros que admiten las consultas y se proporciona un ejemplo de la respuesta
en formato JSON y CSV.

Por ejemplo, la siguiente consulta a la interfaz HTTP
`TIME_SERIES_WEEKLY_ADJUSTED`:

```bash
curl https://www.alphavantage.co/query\?function=TIME_SERIES_WEEKLY_ADJUSTED\
\&symbol=IBM\&outputsize=compact\&apikey=MY_ALPHA_VANTAGE_API_KEY > IBM.json
```

devuelve información bursátil de la empresa IBM para las últimas 100 sesiones en
formato JSON.

:warning: Para utilizar la API de Alpha Vantage sin restricciones es necesario
obtener una [*API Key* gratuita](https://www.alphavantage.co/support/#api-key)
(`MY_ALPHA_VANTAGE_API_KEY`).

## Símbolos (*Tickers*)

Uno de los parámetros requeridos por las consultas a la interfaz HTTP
`TIME_SERIES_WEEKLY_ADJUSTED` es el símbolo.

Un símbolo o código bursátil, también conocido como *ticker* en inglés, es un
código alfanumérico que sirve para identificar de forma abreviada las acciones
de una determinada empresa que cotiza en un determinado mercado bursátil.

Una de las interfaces HTTP de Alpha Vantage es un *search endpoint* que nos
permite realizar búsquedas sobre el espacio de nombres de los *tickers*. Por
ejemplo, la siguiente consulta nos devuelve la lista de *tickers* para la
compañía Pfizer:

```bash
curl https://www.alphavantage.co/query\?function=SYMBOL_SEARCH\
\&keywords=Pfizer\&apikey=MY_ALPHA_VANTAGE_API_KEY > Pfizer.json
```

### El formato JSON

El formato *JavaScript Object Notation* (JSON) es un formato estándar usado por
muchas interfaces HTTP para procesar datos. De manera simplificada, el formato
JSON se define de forma recursiva a partir de dos tipos básicos, cadenas de
caracteres y números, y dos tipos compuestos, las listas (delimitadas por `[` y
`]`) y los objetos (delimitados por `{` y `}`). Una lista se compone de otras
listas u objetos. A su vez, un objeto es una secuencia de pares clave-valor
separados por comas. La clave debe ser una cadena de caracteres, mientras que el
valor puede ser cualquier otro tipo básico o compuesto.

Por ejemplo:

```json
json_string = """
{
    "firstName": "Jane",
    "lastName": "Doe",
    "hobbies": ["running", "sky diving", "singing"],
    "age": 35,
    "children": [
        {
            "firstName": "Alice",
            "age": 6
        },
        {
            "firstName": "Bob",
            "age": 8
        }
    ]
}
"""
```

La ventaja del formato JSON es que se puede manipular fácilmente como un objeto
Python con el paquete `json`:

```python
>>> import json
>>> json_dict = json.loads(json_string)   # transforma la cadena en un diccionario
>>> print(json_dict['firstName'])   # 'firstName' es una cadena de caracteres
Jane
>>> print(json_dict['hobbies'])   # 'firstName' es una lista de cadenas de caracteres
['running', 'sky diving', 'singing']
>>> print(json_dict['children'])   # 'children' es una lista de diccionarios
[{'firstName': 'Alice', 'age': 6}, {'firstName': 'Bob', 'age': 8}]
```

## Estructura del paquete `teii`

El paquete `teii` contiene un único subpaquete llamado `teii.finance` compuesto de tres módulos:

- `exception.py`: Define las excepciones generadas por el subpaquete en
  presencia de errores.
- `finance.py`: Declara la clase base `FinanceClient()`.
- `timeseries.py`: Declara la clase derivada `TimeSeriesFinanceClient()`.

El archivo `teii/__init__.py` está vacío pero el archivo
`teii/finance/__init__.py` no.

- [ ] ¿Para qué sirve el contenido del archivo `teii/finance/__init__.py`?

## Ejemplo de uso del subpaquete `teii-finance`

El archivo `example.py` es un *script* que ilustra cómo usar el subpaquete
`teii.finance`. Tras importar el subpaquete, este *script* crea una instancia de
la clase `TimeSeriesFinanceClient()`, que consulta la interfaz
`TIME_SERIES_WEEKLY_ADJUSTED` para el *ticker* `AMZN` (Amazon). A continuación,
llama al método `weekly_price()` que devuelve una serie de Pandas con el precio
de cierre semanal de dicha compañía. Por último, el *script* dibuja una gráfica
a partir de la serie de Pandas.

- [ ] ¿Por qué no se muestra ningún mensaje de *logging* al ejecutar
  `example.py`?

## Referencias

- [Wikipedia • Tickers](https://en.wikipedia.org/wiki/Ticker_symbol)
- [Wikipedia • JSON](https://en.wikipedia.org/wiki/JSON)
- [Python Documentation • `json` — JSON encoder and decoder](https://docs.python.org/3.7/library/json.html)
- [Real Python • Working With JSON Data in Python](https://realpython.com/python-json/)
