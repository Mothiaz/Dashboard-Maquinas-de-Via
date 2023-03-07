import pandas as pd
from dash import Dash, dcc, html, ctx

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_types: list[str] = data[DataSchema.TIPO].tolist()
    unique_types: list[str] = sorted(set(all_types))

    # @app.callback(
    #     Output(ids.EQUIPMENT_TYPE, 'value'),
    #     [Input(ids.DATE_RANGE, 'start_date'),
    #      Input(ids.DATE_RANGE, 'end_date'),],
    # )
    #
    # def select_all(start_date: str, end_date: str) -> list[str]:
    #     filtered_data = data.query('date >= @start_date and date <= @end_date')
    #     return sorted(set(filtered_data[DataSchema.TIPO].tolist()))

    return html.Div(
        children=[
            html.H6('Tipo'),
            dcc.Checklist(
                id=ids.EQUIPMENT_TYPE,
                options=[{'label': tipo, 'value': tipo}
                         for tipo in unique_types],
                value=[''],
            ),
        ]
    )

