import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # 1) Cargar datos
    df = pd.read_csv("epa-sea-level.csv")

    # 2) Dispersión base
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"], s=10)

    # 3) Línea de mejor ajuste (todos los datos) hasta 2050
    res_all = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    x_all = pd.Series(range(int(df["Year"].min()), 2051))
    y_all = res_all.slope * x_all + res_all.intercept
    ax.plot(x_all, y_all, label="Fit: 1880–2014")

    # 4) Línea de mejor ajuste (desde 2000) hasta 2050
    df_2000 = df[df["Year"] >= 2000]
    res_2000 = linregress(df_2000["Year"], df_2000["CSIRO Adjusted Sea Level"])
    x_2000 = pd.Series(range(2000, 2051))
    y_2000 = res_2000.slope * x_2000 + res_2000.intercept
    ax.plot(x_2000, y_2000, label="Fit: 2000–most recent")

    # 5) Etiquetas y título
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")
    ax.legend()

    # 6) Guardar y retornar figura
    fig.savefig("sea_level_plot.png")
    return fig

# Permite ejecutar localmente
if __name__ == "__main__":
    try:
        draw_plot()
        print("Figura generada: sea_level_plot.png")
    except FileNotFoundError:
        print("⚠️  No se encontró 'epa-sea-level.csv' en la raíz. En freeCodeCamp sí existirá.")
