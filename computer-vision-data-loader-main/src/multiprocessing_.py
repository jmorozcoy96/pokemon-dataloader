import os
import requests
from multiprocessing import Pool
import utils


def download_pokemon(args):
    """Descarga un Pokémon usando multiprocessing."""
    row, output_dir = args
    name = row["Pokemon"]
    sprite = row["Sprite"]
    type1 = row["Type1"]

    # Crear carpeta del tipo si no existe
    type_dir = os.path.join(output_dir, type1)
    utils.maybe_create_dir(type_dir)

    outpath = os.path.join(type_dir, f"{name}.png")

    if not os.path.exists(outpath):
        try:
            r = requests.get(sprite, timeout=10)
            if r.status_code == 200:
                utils.write_binary(outpath, r.content)
                print(f"{name} descargado en {outpath}")
            else:
                print(f"No se pudo descargar sprite de {name}, status={r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error descargando {name}: {e}")


@utils.timeit
def main(output_dir, inputs):
    """Coordina la descarga con multiprocessing."""
    # Preparar directorio
    utils.maybe_remove_dir(output_dir)
    utils.maybe_create_dir(output_dir)

    # Leer pokemons de los CSV
    pokemons = list(utils.read_pokemons(inputs))
    args = [(row, output_dir) for row in pokemons]

    # Multiprocessing Pool
    with Pool() as pool:
        pool.map(download_pokemon, args)

    print("Descarga finalizada con multiprocessing")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directorio para almacenar los datos")
    parser.add_argument("inputs", nargs="+", help="lista de archivos CSV con metadatos")
    args = parser.parse_args()

    main(args.output_dir, args.inputs)