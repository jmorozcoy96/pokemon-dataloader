# src/loader.py
import os
import io
from typing import Iterator, NamedTuple, List
from PIL import Image

from . import utils
from . import sequential_
from . import threading_
from . import asyncio_ 
from . import multiprocessing_


class Row(NamedTuple):
    name: str
    type1: str
    image: Image.Image


def load(inputs: List[str], method: str = "sequential", output_dir: str = "./outputs") -> Iterator[Row]:
    """Carga imágenes de pokemons desde URLs especificadas en archivos CSV."""

    # 1. Descargar sprites según método
    if method == "sequential":
        sequential_.main(output_dir, inputs)
    elif method == "threading":
        threading_.main(output_dir, inputs)
    elif method == "asyncio":
        asyncio_.main(output_dir, inputs)
    elif method == "multiprocessing":
        multiprocessing_.main(output_dir, inputs)
    else:
        raise ValueError(f"Unknown method: {method}")

    # 2. Iterar sobre los pokemons descargados
    for row in utils.read_pokemons(inputs):
        filepath = os.path.join(output_dir, row["Type1"], f"{row['Pokemon']}.png")
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                img = Image.open(io.BytesIO(f.read())).convert("RGBA")
            yield Row(name=row["Pokemon"], type1=row["Type1"], image=img)
