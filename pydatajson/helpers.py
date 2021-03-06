#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Métodos auxiliares"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement

import datetime
import os


def ensure_dir_exists(directory):
    """Se asegura de que un directorio exista."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def traverse_dict(dicc, keys, default_value=None):
    """Recorre un diccionario siguiendo una lista de claves, y devuelve
    default_value en caso de que alguna de ellas no exista.

    Args:
        dicc (dict): Diccionario a ser recorrido.
        keys (list): Lista de claves a ser recorrida. Puede contener
            índices de listas y claves de diccionarios mezcladas.
        default_value: Valor devuelto en caso de que `dicc` no se pueda
            recorrer siguiendo secuencialmente la lista de `keys` hasta
            el final.

    Returns:
        object: El valor obtenido siguiendo la lista de `keys` dentro de
        `dicc`.
    """
    for key in keys:
        if isinstance(dicc, dict) and key in dicc:
            dicc = dicc[key]
        elif (isinstance(dicc, list)
              and isinstance(key, int)
              and key < len(dicc)):
            dicc = dicc[key]
        else:
            return default_value

    return dicc


def is_list_of_matching_dicts(list_of_dicts, expected_keys=None):
    """Comprueba que una lista esté compuesta únicamente por diccionarios,
    que comparten exactamente las mismas claves.

    Args:
        list_of_dicts (list): Lista de diccionarios a comparar.
        expected_keys (set): Conjunto de las claves que cada diccionario debe
            tener. Si no se incluye, se asume que son las claves del primer
            diccionario de la lista.

    Returns:
        bool: True si todos los diccionarios comparten sus claves.
    """

    is_not_list_msg = """
{} no es una lista. Debe ingresar una lista""".format(list_of_dicts)
    assert isinstance(list_of_dicts, list), is_not_list_msg

    not_all_dicts_msg = """
No todos los elementos de {} son diccionarios. Ingrese una lista compuesta
solo por diccionarios.""".format(list_of_dicts)
    assert all([isinstance(d, dict) for d in list_of_dicts]), not_all_dicts_msg

    # Si no se pasan expected_keys, se las toma del primer diccionario
    expected_keys = expected_keys or set(list_of_dicts[0].keys())

    elements = [set(d.keys()) == expected_keys for d in list_of_dicts]

    return all(elements)


def parse_value(cell):
    """Extrae el valor de una celda de Excel como texto."""
    value = cell.value

    # stripea espacios en strings
    if isinstance(value, (str, unicode)):
        value = value.strip()

    # convierte a texto ISO 8601 las fechas
    if isinstance(value, (datetime.datetime)):
        value = value.isoformat()

    return value


def sheet_to_table(worksheet):
    """Transforma una hoja de libro de Excel en una lista de diccionarios.

    Args:
        worksheet (Workbook.worksheet): Hoja de cálculo de un archivo XLSX
            según los lee `openpyxl`

    Returns:
        list_of_dicts: Lista de diccionarios, con tantos elementos como
        registros incluya la hoja, y con tantas claves por diccionario como
        campos tenga la hoja.
    """

    worksheet_rows = list(worksheet.rows)
    headers = [parse_value(cell) for cell in worksheet_rows[0]]
    value_rows = [
        [parse_value(cell) for cell in row] for row in worksheet_rows[1:]
        # Únicamente considero filas con al menos un campo no-nulo
        if any([parse_value(cell) for cell in row])
    ]
    table = [
        # Ignoro los campos con valores nulos (None)
        {k: v for (k, v) in zip(headers, row) if v is not None}
        for row in value_rows
    ]

    return table


def string_to_list(string, sep=","):
    """Transforma una string con elementos separados por `sep` en una lista."""
    return [value.strip() for value in string.split(sep)]


def add_dicts(one_dict, other_dict):
    """Suma clave a clave los dos diccionarios. Si algún valor es un
    diccionario, llama recursivamente a la función. Ambos diccionarios deben
    tener exactamente las mismas claves, y los valores asociados deben ser
    sumables, o diccionarios.

    Args:
        one_dict (dict)
        other_dict (dict)

    Returns:
        dict: resultado de la suma
    """
    result = other_dict.copy()
    for k, v in one_dict.items():
        if isinstance(v, dict):
            result[k] = add_dicts(v, other_dict.get(k, {}))
        else:
            result[k] = result.get(k, 0) + v

    return result


def parse_repeating_time_interval(date_str):
    """Parsea un string con un intervalo de tiempo con repetición especificado
    por la norma ISO 8601 en una cantidad de días que representa ese intervalo.
    Devuelve 0 en caso de que el intervalo sea inválido.
    """
    intervals = {
        'Y': 365,
        'M': 30,
        'W': 7,
        'D': 1,
        'H': 0,
        'S': 0
    }

    if date_str.find('R/P') != 0:  # Periodicity mal formada
        return 0

    date_str = date_str.strip('R/P')
    days = 0
    index = 0
    for interval in intervals:
        value_end = date_str.find(interval)
        if value_end < 0:
            continue
        try:
            days += int(float(date_str[index:value_end]) * intervals[interval])
        # Valor de accrualPeriodicity inválido, se toma como 0
        except ValueError:
            continue
        index = value_end

    # Si el número de días es menor lo redondeamos a 1
    return max(days, 1)
