# 🌊 Sea‑Level Predictor

> Predice niveles del mar futuros a partir de datos históricos con regresión lineal. Proyecto enfocado en **limpieza de datos**, **visualización** y **modelado predictivo** usando **Python**, **pandas** y **matplotlib**.

---

![Sea Level Plot](./sea_level_plot.png)

<p align="center">
  <em>Salida esperada: datos históricos (puntos), tendencia global (línea roja) y tendencia desde 2000 (línea verde).</em>
</p>

---

## 📌 Resumen del Proyecto

Este repositorio analiza el aumento del nivel del mar utilizando el dataset de la **U.S. Environmental Protection Agency (EPA)**. Se ajustan **dos modelos de regresión lineal**:

1. **Regresión global** con todos los datos (1880–2013).
2. **Regresión reciente** usando solo datos desde 2000.

Con ambos modelos se **visualizan tendencias** y se **predicen niveles del mar hasta 2050**.

---

## 🧰 Stack Tecnológico

| Herramienta            | Uso                      |
| ---------------------- | ------------------------ |
| Python 3.x             | Lenguaje principal       |
| pandas                 | Manipulación de datos    |
| matplotlib             | Gráficas y visualización |
| scipy.stats.linregress | Regresión lineal         |

---

## 📁 Estructura de Archivos

```
Sea-Level-Predictor/
├── sea_level_predictor.py      # Script principal (CLI con argparse)
├── epa-sea-level.csv           # Dataset EPA
├── sea_level_plot.png          # Gráfico de salida (autogenerado)
├── requirements.txt            # Dependencias exactas
├── .gitignore                  # Python, venv, cache, plots
└── README.md                   # Documentación del proyecto
```

> Sugerencia: incluye `requirements.txt` y `.gitignore` (ver secciones más abajo) para mejor reproducibilidad.

---

## 🚀 Cómo Ejecutar

### 1) Clonar el repositorio

```bash
git clone https://github.com/your-username/Sea-Level-Predictor.git
cd Sea-Level-Predictor
```

### 2) (Opcional pero recomendado) Crear entorno virtual

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
# o, si prefieres
pip install pandas matplotlib scipy
```

### 4) Ejecutar el script

```bash
python sea_level_predictor.py --input epa-sea-level.csv --output sea_level_plot.png --predict_to 2050
```

### 5) Ver el resultado

El gráfico se guardará como **`sea_level_plot.png`** mostrando los datos históricos y las predicciones.

---

## 🧪 Uso del Script (CLI)

El script expone una interfaz de línea de comandos simple:

```bash
python sea_level_predictor.py \
  --input epa-sea-level.csv \
  --output sea_level_plot.png \
  --predict_to 2050 \
  --dpi 140 \
  --style default
```

**Parámetros**

* `--input` (str): ruta al CSV de la EPA.
* `--output` (str): nombre del archivo de imagen a guardar.
* `--predict_to` (int): último año para proyectar (p. ej., 2050).
* `--dpi` (int, opcional): resolución del gráfico.
* `--style` (str, opcional): estilo de matplotlib (p. ej., `default`, `ggplot`, `seaborn-v0_8`).

---

## ✅ Características Clave

* Código limpio, reproducible y modular.
* Dos modelos de regresión (global y desde 2000) para comparar tendencias.
* Predicciones hasta un año objetivo configurable.
* Visualizaciones claras y exportables a PNG.

---

## 📊 Metodología

1. **Carga y validación** del CSV (columnas esperadas: `Year`, `CSIRO Adjusted Sea Level`).
2. **Ajuste** de regresión lineal con `linregress` para:

   * 1880–2013 (todos los datos)
   * 2000–2013 (subconjunto reciente)
3. **Proyección** de ambas rectas hasta el año `--predict_to`.
4. **Visualización** de puntos históricos y líneas de tendencia.

> Nota: puedes extender a otros modelos (p. ej., regresión polinómica o ARIMA) si detectas no‑linealidades.

---

## 📦 requirements.txt (recomendado)

Incluye un archivo `requirements.txt` similar a:

```txt
pandas>=2.0,<3
matplotlib>=3.7,<4
scipy>=1.10,<2
```

---

## 🙈 .gitignore sugerido

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg-info/
.venv/

# OS
.DS_Store
Thumbs.db

# Plots & outputs
*.png
!sea_level_plot.png
```

---

## 👩‍💻 Código Base Sugerido (extracto)

> El repositorio original usa un script único. Aquí un extracto con buenas prácticas (argparse, funciones puras y tipado):

```python
# sea_level_predictor.py
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


@dataclass
class RegressionResult:
    slope: float
    intercept: float


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Normaliza nombres esperados del dataset de la EPA
    assert {"Year", "CSIRO Adjusted Sea Level"}.issubset(df.columns), (
        "El CSV debe contener 'Year' y 'CSIRO Adjusted Sea Level'."
    )
    df = df.rename(columns={"CSIRO Adjusted Sea Level": "sea_level"})
    df = df[["Year", "sea_level"]].dropna()
    return df


def fit_regression(x: pd.Series, y: pd.Series) -> RegressionResult:
    r = linregress(x, y)
    return RegressionResult(slope=r.slope, intercept=r.intercept)


def predict(years: pd.Series, reg: RegressionResult) -> pd.Series:
    return reg.slope * years + reg.intercept


def plot(df: pd.DataFrame, reg_all: RegressionResult, reg_2000: RegressionResult,
         predict_to: int, output: Path, dpi: int = 140, style: str = "default") -> None:
    plt.style.use(style)

    # Eje X extendido para proyección
    years_all = pd.Series(range(int(df["Year"].min()), predict_to + 1))
    years_2000 = pd.Series(range(2000, predict_to + 1))

    # Predicciones
    yhat_all = predict(years_all, reg_all)
    yhat_2000 = predict(years_2000, reg_2000)

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Year"], df["sea_level"], alpha=0.7, label="Datos históricos")
    ax.plot(years_all, yhat_all, color="red", linewidth=2, label="Regresión 1880–2013")
    ax.plot(years_2000, yhat_2000, color="green", linewidth=2, label="Regresión 2000–2013")

    ax.set_xlabel("Año")
    ax.set_ylabel("Nivel del mar (pulgadas)")
    ax.set_title("Predicción del nivel del mar")
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.4)

    fig.tight_layout()
    fig.savefig(output, dpi=dpi)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Sea-Level Predictor")
    p.add_argument("--input", type=Path, default=Path("epa-sea-level.csv"))
    p.add_argument("--output", type=Path, default=Path("sea_level_plot.png"))
    p.add_argument("--predict_to", type=int, default=2050)
    p.add_argument("--dpi", type=int, default=140)
    p.add_argument("--style", type=str, default="default")
    args = p.parse_args()

    df = load_data(args.input)
    reg_all = fit_regression(df["Year"], df["sea_level"])  # 1880–2013
    df_recent = df[df["Year"] >= 2000]
    reg_2000 = fit_regression(df_recent["Year"], df_recent["sea_level"])  # 2000–2013

    plot(df, reg_all, reg_2000, args.predict_to, args.output, dpi=args.dpi, style=args.style)


if __name__ == "__main__":
    main()
```

> Para un proyecto más grande, separa en módulos: `data.py`, `model.py`, `viz.py`, `cli.py`.

---

## 🧠 Qué Aprenderás

* Aplicar **regresión lineal** a series de tiempo simples.
* Visualizar **tendencias** y **proyecciones**.
* Estructurar un **proyecto de ciencia de datos** claro y extensible.

---

## 🌍 Aplicaciones Reales

* Análisis de **cambio climático**.
* Modelado de **datos ambientales**.
* **Analítica predictiva** para políticas públicas.

---

## 🗃️ Fuente de Datos

* EPA: *Global Mean Sea Level* (GMSL). Asegúrate de incluir atribución y enlace al dataset original si lo publicas.

---

## 🔬 Extensiones Sugeridas

* Intervalos de **confianza** para ambas rectas.
* **Pruebas unitarias** (pytest) para funciones puras.
* Exportar resultados a **CSV/Parquet** con las predicciones.
* **Regresión robusta** o modelos no lineales si aparecen outliers.
* Pipeline reproducible con **Makefile** o **nox/pytest**.

---

## 🤝 Contribuciones

¡Contribuciones son bienvenidas! Abre un **issue** o un **pull request** con una descripción clara.

---

## 📄 Licencia

Sugerida: **MIT License**. Añade un archivo `LICENSE` en la raíz del repo.

---

## 🙋 Contacto

Creado por **Emanuel González Michea**.
