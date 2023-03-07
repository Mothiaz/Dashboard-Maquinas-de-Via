import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_items: list[str] = data[DataSchema.ITEM].tolist()
    unique_items: list[str] = sorted(set(all_items))

    @app.callback(
        Output(ids.ITEM_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_ITEMS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_ITEMS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.SET_DROPDOWN, 'value')]
    )
    def update_value(_int1, _int2,
                     start_date: str, end_date: str,
                     conjuntos: list[str]) -> list[str]:
        button_clicked = ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_ITEMS_BUTTON:
            return ['']
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date '
                                       'and conjunto in @conjuntos')
            return sorted(set(filtered_data[DataSchema.ITEM].tolist()))

    @app.callback(
        Output(ids.ITEM_DROPDOWN, 'options'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.SET_DROPDOWN, 'value')]
    )
    def update_options(start_date: str, end_date: str,
                       conjuntos: list[str]) -> list[str]:
        filtered_data = data.query('date >= @start_date and date <= @end_date '
                                   'and conjunto in @conjuntos')
        return sorted(set(filtered_data[DataSchema.ITEM].tolist()))

    return html.Div(
        children=[
            html.H6('Items'),
            dcc.Dropdown(
                id=ids.ITEM_DROPDOWN,
                options=[{'label': item, 'value': item} for item in unique_items],
                value=unique_items,
                multi=True,
                placeholder='Select',
            ),
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_ITEMS_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className='dropdown-button',
                children=['Select None'],
                id=ids.SELECT_NULL_ITEMS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
