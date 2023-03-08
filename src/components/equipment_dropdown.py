import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_equipments: list[str] = data[DataSchema.EQUIPMENT].tolist()
    unique_equipments: list[str] = sorted(set(all_equipments))

    @app.callback(
        Output(ids.EQUIPMENT_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_EQUIPS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_EQUIPS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.EVENT_TYPE, 'value'),
         Input(ids.FLEET_DROPDOWN, 'value'), ],
    )
    def update_value(_int1, _int2,
                     start_date: str, end_date: str,
                     event: list[str], fleets: list[str]) -> list[str]:
        button_clicked = ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_EQUIPS_BUTTON:
            return []
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date '
                                       'and event in @event and fleet in @fleets')
            return sorted(set(filtered_data[DataSchema.EQUIPMENT].tolist()))

    @app.callback(
        Output(ids.EQUIPMENT_DROPDOWN, 'options'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.EVENT_TYPE, 'value'),
         Input(ids.FLEET_DROPDOWN, 'value'), ],
    )
    def update_options(start_date: str, end_date: str,
                       event: list[str], fleets: list[str]) -> list[str]:
        filtered_data = data.query('date >= @start_date and date <= @end_date '
                                   'and event in @event and fleet in @fleets')
        return sorted(set(filtered_data[DataSchema.EQUIPMENT].tolist()))

    return html.Div(
        children=[
            html.H6('Equipment'),
            dcc.Dropdown(
                id=ids.EQUIPMENT_DROPDOWN,
                options=[{'label': equipment, 'value': equipment}
                         for equipment in unique_equipments],
                value=unique_equipments,
                multi=True,
                placeholder='Select',
            ),
            dbc.Button(
                className='m-1',
                size='sm',
                children=['Select All'],
                id=ids.SELECT_ALL_EQUIPS_BUTTON,
                n_clicks=0,
            ),
            dbc.Button(
                className='m-1',
                size='sm',
                children=['Select None'],
                id=ids.SELECT_NULL_EQUIPS_BUTTON,
                n_clicks=0,
            )
        ],
    )
