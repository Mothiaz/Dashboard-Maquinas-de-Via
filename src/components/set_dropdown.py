import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from data.loader import DataSchema
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_sets: list[str] = data[DataSchema.SET].tolist()
    unique_sets: list[str] = sorted(set(all_sets))

    @app.callback(
        Output(ids.SET_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_SETS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_SETS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.SYSTEM_DROPDOWN, 'value')]
    )

    def update_value(_int1, _int2,
                     start_date: str, end_date: str,
                     systems: list[str]) -> list[str]:
        button_clicked =ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_SETS_BUTTON:
            return ['']
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date '
                                       'and system in @systems')
            return sorted(set(filtered_data[DataSchema.SET].tolist()))


    return html.Div(
        children=[
            html.H6('Sets'),
            dcc.Dropdown(
                id=ids.SET_DROPDOWN,
                options=[{'label': set, 'value': set} for set in unique_sets],
                value=unique_sets,
                multi=True,
                placeholder='Select',
            ),
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_SETS_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className='dropdown-button',
                children=['Select None'],
                id=ids.SELECT_NULL_SETS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
