# tests/test_benchmark.py
import time
import plotly.express as px
from src import loader


def run_benchmark():
    inputs = ["./data/pokemon-gen1-data.csv"]
    methods = ["sequential", "threading", "asyncio", "multiprocessing"]

    results = []

    for method in methods:
        print(f"\n>>> Ejecutando método: {method}")
        t0 = time.perf_counter()

        # Cargar primer sprite para forzar la descarga
        iterator = loader.load(inputs, method=method, output_dir=f"./outputs_{method}")
        _ = next(iterator)

        elapsed = time.perf_counter() - t0
        results.append({"method": method, "time": elapsed})
        print(f"{method}: {elapsed:.4f} segundos")

    return results


def save_results_html(results, outpath="tests/benchmark_results.html"):
    fig = px.bar(
        results,
        x="method",
        y="time",
        title="Desempeño de métodos de carga de Pokémon",
        labels={"method": "Método", "time": "Tiempo (s)"},
        text="time"
    )
    fig.update_traces(texttemplate="%{text:.4f}s", textposition="outside")
    fig.write_html(outpath)
    print(f"\n✅ Resultados guardados en {outpath}")


if __name__ == "__main__":
    results = run_benchmark()
    save_results_html(results)