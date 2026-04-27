# CLI de consulta rápida

Este fichero documenta `cli.py`, una capa ligera para consultar cálculos de salario sin generar el Excel masivo.

## Requisitos

Instala las dependencias del proyecto:

```bash
python3 -m pip install -r requirements.txt
```

## Ayuda

```bash
python3 cli.py --help
```

## Calcular un salario

Calcula el desglose para un bruto anual concreto. Por defecto usa el año 2026 y 12 pagas.

```bash
python3 cli.py salario 30000
```

Salida:

```text
Año  | Bruto anual | Coste empresa | SS empresa | SS trabajador | IRPF       | Neto anual  | Neto mensual (12p)
-----+-------------+---------------+------------+---------------+------------+-------------+-------------------
2026 | 30,000.00 € |   39,645.00 € | 9,645.00 € |    1,950.00 € | 4,926.00 € | 23,124.00 € |         1,927.00 €
```

Con año y número de pagas:

```bash
python3 cli.py salario 50000 --anio 2026 --pagas 14
```

Salida:

```text
Año  | Bruto anual | Coste empresa | SS empresa  | SS trabajador | IRPF        | Neto anual  | Neto mensual (14p)
-----+-------------+---------------+-------------+---------------+-------------+-------------+-------------------
2026 | 50,000.00 € |   66,075.00 € | 16,075.00 € |    3,250.00 € | 11,204.50 € | 35,545.50 € |         2,538.96 €
```

## Tabla por rango salarial

Genera una tabla pequeña entre dos brutos, con el salto indicado.

```bash
python3 cli.py tabla --anio 2026 --desde 20000 --hasta 40000 --paso 10000
```

Salida:

```text
Año  | Bruto anual | Coste empresa | SS empresa  | SS trabajador | IRPF       | Neto anual  | Neto mensual (12p)
-----+-------------+---------------+-------------+---------------+------------+-------------+-------------------
2026 | 20,000.00 € |   26,430.00 € |  6,430.00 € |    1,300.00 € | 1,773.32 € | 16,926.68 € |         1,410.56 €
2026 | 30,000.00 € |   39,645.00 € |  9,645.00 € |    1,950.00 € | 4,926.00 € | 23,124.00 € |         1,927.00 €
2026 | 40,000.00 € |   52,860.00 € | 12,860.00 € |    2,600.00 € | 7,745.00 € | 29,655.00 € |         2,471.25 €
```

## Comparar años

Compara el mismo bruto nominal entre varios años.

```bash
python3 cli.py comparar 30000 --desde-anio 2024 --hasta-anio 2026
```

Salida:

```text
Año  | Bruto anual | Coste empresa | SS empresa | SS trabajador | IRPF       | Neto anual  | Neto mensual (12p)
-----+-------------+---------------+------------+---------------+------------+-------------+-------------------
2024 | 30,000.00 € |   39,594.00 € | 9,594.00 € |    1,941.00 € | 4,928.70 € | 23,130.30 € |         1,927.52 €
2025 | 30,000.00 € |   39,621.00 € | 9,621.00 € |    1,944.00 € | 4,927.80 € | 23,128.20 € |         1,927.35 €
2026 | 30,000.00 € |   39,645.00 € | 9,645.00 € |    1,950.00 € | 4,926.00 € | 23,124.00 € |         1,927.00 €
```

## Ejecutar como script

`cli.py` puede ejecutarse directamente si tiene permisos de ejecución:

```bash
./cli.py salario 30000 --anio 2026
```

La salida es equivalente a `python3 cli.py salario 30000 --anio 2026`.

## Nota

El CLI reutiliza las funciones de `Calculo_Salario_IRPF.py`, pero evita ejecutar la sección final que genera `Auditoria_Integral_Nominas_e_Inflacion_2012_2026.xlsx`.

## Validación

Para comprobar que el CLI devuelve resultados coherentes con el Excel masivo, se generó localmente el archivo completo ejecutando:

```bash
python3 Calculo_Salario_IRPF.py
```

Resultado de la validación:

```text
Archivo generado: Auditoria_Integral_Nominas_e_Inflacion_2012_2026.xlsx
Tamaño aproximado: 144.8 MB
Hojas: 18
DAT_2012, DAT_2024, DAT_2025, DAT_2026: 100002 filas cada una, incluyendo cabecera
```

También se compararon filas representativas del Excel contra el motor usado por el CLI:

```text
OK DAT_2026 bruto 30000: neto 23,124.00 €
OK DAT_2026 bruto 50000: neto 35,545.50 €
OK DAT_2025 bruto 30000: neto 23,128.20 €
OK DAT_2024 bruto 30000: neto 23,130.30 €
OK DAT_2012 bruto 30000: neto 22,666.59 €
VALIDACION_OK
```

El Excel masivo no se incluye en el repositorio porque es un artefacto pesado y reproducible.
