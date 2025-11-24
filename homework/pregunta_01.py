# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import os
import zipfile
import pandas as pd

def descomprimir_zip(ruta_zip, ruta_destino):
    """Descomprime el ZIP y asegura que las carpetas train/test queden en la ruta correcta."""
    if os.path.exists(os.path.join(ruta_destino, "train")):
        return

    if not os.path.exists(ruta_zip):
        raise FileNotFoundError(f"No se encontró el archivo {ruta_zip}")

    # Descomprime todo
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        zip_ref.extractall(ruta_destino)

    raiz_extra = os.path.join(ruta_destino, "input")
    if os.path.exists(raiz_extra):
        for item in os.listdir(raiz_extra):
            src = os.path.join(raiz_extra, item)
            dst = os.path.join(ruta_destino, item)
            os.rename(src, dst)
        os.rmdir(raiz_extra)

    print(f"ZIP descomprimido en {ruta_destino}")


def procesar_dataset(ruta_base, salida_csv):
    frases = []
    targets = []

    if not os.path.exists(ruta_base):
        raise FileNotFoundError(f"No existe la carpeta {ruta_base}")

    for sentimiento in ["negative", "positive", "neutral"]:
        ruta_sentimiento = os.path.join(ruta_base, sentimiento)
        if not os.path.exists(ruta_sentimiento):
            continue

        # Leemos archivos en orden alfabético para consistencia
        for archivo in sorted(os.listdir(ruta_sentimiento)):
            if archivo.endswith(".txt"):
                ruta_archivo = os.path.join(ruta_sentimiento, archivo)
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    texto = f.read().strip()
                    if texto:  
                        frases.append(texto)
                        targets.append(sentimiento.lower().strip())

    if not frases:
        raise ValueError(f"No se encontraron archivos de texto en {ruta_base}")

    df = pd.DataFrame({
        "phrase": frases,
        "target": targets
    })

    os.makedirs(os.path.dirname(salida_csv), exist_ok=True)
    df.to_csv(salida_csv, index=False)
    print(f"Archivo generado: {salida_csv}")


def pregunta_01():
    descomprimir_zip("files/input.zip", "files/input")

    procesar_dataset(os.path.join("files", "input", "train"),
                     os.path.join("files", "output", "train_dataset.csv"))
    procesar_dataset(os.path.join("files", "input", "test"),
                     os.path.join("files", "output", "test_dataset.csv"))
