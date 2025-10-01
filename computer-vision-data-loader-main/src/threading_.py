import os
import shutil
import threading
import requests
import utils
import time


def download_pokemon(row, output_dir, session):
    name = row["Pokemon"]
    sprite = row["Sprite"]
    type1 = row["Type1"]

    # Crear carpeta por tipo si no existe
    type_dir = os.path.join(output_dir, type1)
    utils.maybe_create_dir(type_dir)

    outpath = os.path.join(type_dir, f"{name}.png")

    # Evitar descargar si ya existe
    if not os.path.exists(outpath):
        for attempt in range(3):  # hasta 3 intentos en caso de error
            try:
                content = utils.maybe_download_sprite(session, sprite)
                if content:
                    utils.write_binary(outpath, content)
                    print(f"{name} descargado en {outpath}")
                else:
                    print(f"No se pudo descargar sprite de {name}")
                break
            except requests.exceptions.SSLError:
                print(f"SSL error con {name}, intento {attempt+1}/3")
                time.sleep(2)
            except Exception as e:
                print(f"Error descargando {name}: {e}")
                break


@utils.timeit
def main(output_dir, inputs):
    # Borrar y recrear directorio de salida
    utils.maybe_remove_dir(output_dir)
    utils.maybe_create_dir(output_dir)

    pokemons = list(utils.read_pokemons(inputs))
    threads = []

    with requests.Session() as session:
        for row in pokemons:
            t = threading.Thread(target=download_pokemon, args=(row, output_dir, session))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    print("Descarga finalizada con threads")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directory to store the data")
    parser.add_argument("inputs", nargs="+", help="list of files with metadata")
    args = parser.parse_args()

    main(args.output_dir, args.inputs)
