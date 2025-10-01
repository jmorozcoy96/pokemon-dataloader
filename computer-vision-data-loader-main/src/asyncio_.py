import os
import aiohttp
import asyncio
import utils
import time


async def download_pokemon(session, row, output_dir):
    """Descarga un Pokémon de forma asíncrona."""
    name = row["Pokemon"]
    sprite = row["Sprite"]
    type1 = row["Type1"]

    # Crear carpeta por tipo
    type_dir = os.path.join(output_dir, type1)
    utils.maybe_create_dir(type_dir)

    outpath = os.path.join(type_dir, f"{name}.png")

    # Evitar re-descarga
    if not os.path.exists(outpath):
        for attempt in range(3):  # hasta 3 intentos
            try:
                async with session.get(sprite) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        utils.write_binary(outpath, content)
                        print(f"{name} descargado en {outpath}")
                    else:
                        print(f"No se pudo descargar sprite de {name}, status={resp.status}")
                break
            except aiohttp.ClientSSLError:
                print(f"SSL error con {name}, intento {attempt+1}/3")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error descargando {name}: {e}")
                break


@utils.timeit
def main(output_dir, inputs):
    """Coordina la descarga asíncrona."""
    # Preparar directorio
    utils.maybe_remove_dir(output_dir)
    utils.maybe_create_dir(output_dir)

    pokemons = list(utils.read_pokemons(inputs))

    async def runner():
        async with aiohttp.ClientSession() as session:
            tasks = [download_pokemon(session, row, output_dir) for row in pokemons]
            await asyncio.gather(*tasks)

    asyncio.run(runner())
    print("Descarga finalizada con asyncio")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directorio para almacenar los datos")
    parser.add_argument("inputs", nargs="+", help="lista de archivos CSV con metadatos")
    args = parser.parse_args()

    main(args.output_dir, args.inputs)