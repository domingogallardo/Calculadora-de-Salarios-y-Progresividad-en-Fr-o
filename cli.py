#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI ligero para consultar el motor fiscal sin generar el Excel masivo."""

import argparse
from pathlib import Path

import numpy as np


SCRIPT_ORIGINAL = Path(__file__).with_name("Calculo_Salario_IRPF.py")
MARCADOR_EJECUCION = "# 6. EJECUCIÓN MAESTRA Y GENERACIÓN DEL EXCEL COMPLETO"


def cargar_motor():
    """Carga funciones y datos del script original evitando su ejecución final."""
    codigo = SCRIPT_ORIGINAL.read_text(encoding="utf-8")
    codigo_motor = codigo.split(MARCADOR_EJECUCION, maxsplit=1)[0]
    namespace = {}
    exec(codigo_motor, namespace)
    return namespace


MOTOR = cargar_motor()


def formatear_euros(valor):
    return f"{valor:,.2f} €"


def calcular_nomina_resumen(bruto, anio, pagas):
    parametros = MOTOR["obtener_parametros"](anio)
    coste, ss_empresa, ss_trabajador, irpf, neto = MOTOR["calcular_nomina_agregada"](
        bruto, anio, parametros
    )
    return {
        "Año": anio,
        "Bruto anual": bruto,
        "Coste empresa": coste,
        "SS empresa": ss_empresa,
        "SS trabajador": ss_trabajador,
        "IRPF": irpf,
        "Neto anual": neto,
        f"Neto mensual ({pagas}p)": neto / pagas,
    }


def imprimir_tabla(filas):
    if not filas:
        print("No hay filas para mostrar.")
        return

    columnas = list(filas[0].keys())
    filas_texto = []
    for fila in filas:
        valores = []
        for columna in columnas:
            valor = fila[columna]
            valores.append(str(valor) if columna == "Año" else formatear_euros(valor))
        filas_texto.append(valores)

    anchos = [
        max(len(str(columna)), *(len(fila[i]) for fila in filas_texto))
        for i, columna in enumerate(columnas)
    ]
    cabecera = " | ".join(str(columna).ljust(anchos[i]) for i, columna in enumerate(columnas))
    separador = "-+-".join("-" * ancho for ancho in anchos)

    print(cabecera)
    print(separador)
    for fila in filas_texto:
        print(" | ".join(valor.rjust(anchos[i]) for i, valor in enumerate(fila)))


def cmd_salario(args):
    imprimir_tabla([calcular_nomina_resumen(args.bruto, args.anio, args.pagas)])


def cmd_tabla(args):
    salarios = np.arange(args.desde, args.hasta + args.paso, args.paso)
    filas = [
        calcular_nomina_resumen(float(bruto), args.anio, args.pagas)
        for bruto in salarios
        if bruto <= args.hasta
    ]
    imprimir_tabla(filas)


def cmd_comparar(args):
    if args.desde_anio > args.hasta_anio:
        raise SystemExit("--desde-anio no puede ser mayor que --hasta-anio")

    filas = [
        calcular_nomina_resumen(args.bruto, anio, args.pagas)
        for anio in range(args.desde_anio, args.hasta_anio + 1)
    ]
    imprimir_tabla(filas)


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Consulta rápida de salario neto, IRPF y Seguridad Social en España (2012-2026)."
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    salario = subparsers.add_parser("salario", help="Calcula una nómina anual concreta.")
    salario.add_argument("bruto", type=float, help="Salario bruto anual.")
    salario.add_argument("--anio", type=int, default=2026, choices=range(2012, 2027), metavar="YYYY")
    salario.add_argument("--pagas", type=int, default=12, help="Número de pagas para el neto mensual.")
    salario.set_defaults(func=cmd_salario)

    tabla = subparsers.add_parser("tabla", help="Genera una tabla ligera por rango salarial.")
    tabla.add_argument("--anio", type=int, default=2026, choices=range(2012, 2027), metavar="YYYY")
    tabla.add_argument("--desde", type=float, default=15000, help="Primer bruto anual.")
    tabla.add_argument("--hasta", type=float, default=100000, help="Último bruto anual.")
    tabla.add_argument("--paso", type=float, default=5000, help="Salto entre salarios.")
    tabla.add_argument("--pagas", type=int, default=12, help="Número de pagas para el neto mensual.")
    tabla.set_defaults(func=cmd_tabla)

    comparar = subparsers.add_parser("comparar", help="Compara un mismo bruto nominal entre años.")
    comparar.add_argument("bruto", type=float, help="Salario bruto anual.")
    comparar.add_argument("--desde-anio", type=int, default=2012, choices=range(2012, 2027), metavar="YYYY")
    comparar.add_argument("--hasta-anio", type=int, default=2026, choices=range(2012, 2027), metavar="YYYY")
    comparar.add_argument("--pagas", type=int, default=12, help="Número de pagas para el neto mensual.")
    comparar.set_defaults(func=cmd_comparar)

    return parser


def main():
    args = crear_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
