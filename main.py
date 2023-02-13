from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP

from src.data.source import DataSource
from src.components.layout import create_layout
from src.data.loader import load_data

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

DATA_PATH = './src/data/perfilperdas.xlsx'

def main() -> None:
    data = load_data(DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Dashboard MV"
    # data = DataSource(data)
    app.layout = create_layout(app, data)

    app.run_server(debug=True, use_reloader=False)


if __name__ == "__main__":
    main()