# Pokémon Data Loader Benchmark

Este proyecto implementa diferentes estrategias para **descargar y cargar sprites de Pokémon** desde metadatos CSV, y compara su rendimiento utilizando distintos modelos de concurrencia en Python:

- **Secuencial (`sequential_.py`)**
- **Threads (`threading_.py`)**
- **Asyncio (`asyncio_.py`)**
- **Multiprocessing (`multiprocessing_.py`)**

Además, se incluye un **benchmark automático** que genera un **reporte en HTML con un gráfico de desempeño**.

---

## 📂 Estructura del repositorio

pokemon-data-loader/
│
├── data/
│ └── pokemon-gen1-data.csv # dataset de ejemplo
├── src/
│ ├── utils.py
│ ├── loader.py
│ ├── sequential_.py
│ ├── threading_.py
│ ├── asyncio_.py
│ └── multiprocessing_.py
├── tests/
│ └── test_benchmark.py # benchmark automático
├── experiment.ipynb # notebook para pruebas
├── README.md
├── pyproject.toml # definición de dependencias
└── uv.lock # lockfile (si usas uv/pip-tools)

Clona el repo y crea un entorno virtual:

```bash
git clone https://github.com/<tu-usuario>/pokemon-data-loader.git
cd pokemon-data-loader
python -m venv venv
source venv/bin/activate   # en Windows: venv\Scripts\activate