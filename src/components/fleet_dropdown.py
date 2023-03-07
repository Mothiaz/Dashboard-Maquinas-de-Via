import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_fleets: list[str] = data[DataSchema.FLEET].tolist()
    unique_fleets: list[str] = sorted(set(all_fleets))

    @app.callback(
        Output(ids.FLEET_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_FLEETS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_FLEETS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.EQUIPMENT_TYPE, 'value'), ],
    )
    def update_value(_int1, _int2, start_date: str, end_date: str, tipo: list[str]) -> list[str]:
        button_clicked = ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_FLEETS_BUTTON:
            return []
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date and tipo in @tipo')
            return sorted(set(filtered_data[DataSchema.FLEET].tolist()))

    @app.callback(
        Output(ids.FLEET_DROPDOWN, 'options'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.EQUIPMENT_TYPE, 'value')],
    )
    def update_options(start_date: str, end_date: str, tipo: list[str]) -> list[str]:
        filtered_data = data.query('date >= @start_date and date <= @end_date and tipo in @tipo')
        return sorted(set(filtered_data[DataSchema.FLEET].tolist()))

    return html.Div(
        children=[
            html.H6('Fleet'),
            dcc.Dropdown(
                id=ids.FLEET_DROPDOWN,
                options=[{'label': fleet, 'value': fleet}
                         for fleet in unique_fleets],
                value=unique_fleets,
                multi=True,
                placeholder='Select'
            ),
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_FLEETS_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className='dropdown-button',
                children=['Select None'],
                id=ids.SELECT_NULL_FLEETS_BUTTON,
                n_clicks=0,
            )
        ]
    )
