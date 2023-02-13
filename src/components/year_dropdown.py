import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
# from ..data.source import DataSource
from . import ids

# render eh a funcao que retorna o html para construcao do objeto do titulo
# neste caso, year_dropdown


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years: list[str] = data[DataSchema.YEAR].tolist()
    unique_years = sorted(set(all_years))

    @app.callback(
        Output(ids.YEAR_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_YEARS_BUTTON, 'n_clicks'),
        Input(ids.DATE_RANGE, 'start_date'),
        Input(ids.DATE_RANGE, 'end_date'),],
    )

    # #funcao que dá o output do callback
    def select_all_years(_: int, start_date, end_date) -> list[str]:
        filtered_data = data.query('date >= @start_date and date <= @end_date')
        return sorted(set(filtered_data[DataSchema.YEAR].tolist()))

    # #retorno da render
    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{'label': year, 'value': year} for year in unique_years],
                value=unique_years,
                multi=True,
            ),
            html.Button(
                className='dropdown-button',
                children=["Select All"],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0,
            )
        ]
    )
