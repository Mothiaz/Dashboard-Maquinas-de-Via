import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
# from ..data.source import DataSource
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_systems: list[str] = data[DataSchema.SYSTEM].tolist()
    unique_systems: list[str] = sorted(set(all_systems))

    @app.callback(
        Output(ids.SYSTEM_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_SYSTEMS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_SYSTEMS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.FLEET_DROPDOWN, 'value'), ],
    )
    def update_value(_int1, _int2, start_date: str, end_date: str, fleets: list[str]) -> list[str]:
        button_clicked = ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_FLEETS_BUTTON:
            return []
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date and fleet in @fleets')
            return sorted(set(filtered_data[DataSchema.SYSTEM].tolist()))

    return html.Div(
        children=[
            html.H6('System'),
            dcc.Dropdown(
                id=ids.SYSTEM_DROPDOWN,
                options=[{'label': system, 'value': system}
                         for system in unique_systems],
                value=unique_systems,
                multi=True,
                placeholder='Select'
            ),
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_SYSTEMS_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className='dropdown-button',
                children=['Select None'],
                id=ids.SELECT_NULL_SYSTEMS_BUTTON,
                n_clicks=0,
            )
        ]
    )
