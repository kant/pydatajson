History
=======

0.1.7 (2017-01-10)
------------------

* Se agrega el módulo `xlsx_to_json`, con dos métodos para lectura de archivos locales o remotos, sean JSON genéricos (`xlsx_to_json.read_json()`) o metadatos de catálogos en formato XLSX (`read_local_xlsx_catalog()`).
* Se agrega el método `pydatajson.read_catalog()` que interpreta todos las representaciones externas o internas de catálogos conocidas, y devuelve un diccionario con sus metadatos.

0.1.6 (2017-01-04)
------------------

* Se incorpora el método `DataJson.generate_harvestable_catalogs()`, que filtra los datasets no deseados de un conjunto de catálogos.
* Se agrega el parámetro `harvest` a los métodos `DataJson.generate_harvestable_catalogs()`, `DataJson.generate_datasets_report()` y `DataJson.generate_harvester_config()`, para controlar el criterio de elección de los datasets a cosechar.
* Se agrega el parámetro `export_path` a los métodos `DataJson.generate_harvestable_catalogs()`, `DataJson.generate_datasets_report()` y `DataJson.generate_harvester_config()`, para controlar la exportación de sus resultados.

0.1.4 (2016-12-23)
------------------

* Se incorpora el método `DataJson.generate_datasets_report()`, que reporta sobre los datasets y la calidad de calidad de metadatos de un conjunto de catálogos.
* Se incorpora el método `DataJson.generate_harvester_config()`, que crea archivos de configuración para el Harvester a partir de los reportes de `generate_datasets_report()`.

0.1.3 (2016-12-19)
------------------

* Al resultado de `DataJson.validate_catalog()` se le incorpora una lista (`"errors"`) con información de los errores encontrados durante la validación en cada nivel de jerarquía ("catalog" y cada elemento de "dataset")

0.1.2 (2016-12-14)
------------------

* Se incorpora validación de tipo y formato de campo
* Los métodos `DataJson.is_valid_catalog()` y `DataJson.validate_catalog()` ahora aceptan un `dict` además de un `path/to/data.json` o una url a un data.json.

0.1.0 (2016-12-01)
------------------

Primera versión para uso productivo del paquete.

* La instalación via `pip install` debería reconocer correctamente la ubicación de los validadores por default.
* El manejo de data.json's ubicados remotamente se hace en función del resultado de `urlparse.urlparse`
* El formato de respuesta de `validate_catalog` se adecúa a la última especificación (ver [`samples/validate_catalog_returns.json`](samples/validate_catalog_returns.json).

0.0.13 (2016-11-25)
-------------------

* Intentar que la instalación del paquete sepa donde están instalados los schemas por default

0.0.12 (2016-11-25)
-------------------

* Primera versión propuesta para v0.1.0