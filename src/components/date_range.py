import pandas as pd
import datetime

import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
# from ..data.source import DataSource
from . import ids

# render eh a funcao que retorna o html para construcao do objeto do titulo
# neste caso, year_dropdown


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_dates: list = data[DataSchema.DATE].tolist()  # #define variavel classe all_years
    unique_dates = sorted(set(all_dates), key=str)
    # classifica com sorted e pega os valores
    # unicos com set()

    # @app.callback(
    #     Output(ids.DATE_RANGE, 'value'),
    #     Input(ids.SELECT_ALL_DATES_BUTTON, 'n_clicks'),
    # )
    # # #funcao que dá o output do callback
    # def select_all_dates(_: int) -> list[str]:
    #     return unique_dates

    #retorno da render
    return html.Div(
        children=[
            html.H6("Year"),
            dcc.DatePickerRange(
                id=ids.DATE_RANGE,
                min_date_allowed=unique_dates[0],
                max_date_allowed=unique_dates[-1],
                start_date=(datetime.date.today()-datetime.timedelta(days=90)),
                end_date=datetime.date.today(),
                display_format='DD/MM/YYYY'
            ),
        ]
    )
