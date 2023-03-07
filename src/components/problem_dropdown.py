import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output

from data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_problems: list[str] = data[DataSchema.PROBLEM].tolist()
    unique_problems: list[str] = sorted(set(all_problems))

    @app.callback(
        Output(ids.PROBLEM_DROPDOWN, 'value'),
        [Input(ids.SELECT_ALL_PROBLEMS_BUTTON, 'n_clicks'),
         Input(ids.SELECT_NULL_PROBLEMS_BUTTON, 'n_clicks'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.ITEM_DROPDOWN, 'value')]
    )
    def update_value(_int1, _int2,
                     start_date: str, end_date: str,
                     items: list[str]) -> list[str]:
        button_clicked = ctx.triggered_id
        if button_clicked == ids.SELECT_NULL_PROBLEMS_BUTTON:
            return ['']
        else:
            filtered_data = data.query('date >= @start_date and date <= @end_date '
                                       'and item in @items')
            return sorted(set(filtered_data[DataSchema.PROBLEM].tolist()))

    @app.callback(
        Output(ids.PROBLEM_DROPDOWN, 'options'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.ITEM_DROPDOWN, 'value')]
    )
    def update_options(start_date: str, end_date: str,
                       items: list[str]) -> list[str]:
        filtered_data = data.query('date >= @start_date and date <= @end_date '
                                   'and item in @items')
        return sorted(set(filtered_data[DataSchema.PROBLEM].tolist()))

    return html.Div(
        children=[
            html.H6('Problems'),
            dcc.Dropdown(
                id=ids.PROBLEM_DROPDOWN,
                options=[{'label': problem, 'value': problem} for problem in unique_problems],
                value=unique_problems,
                multi=True,
                placeholder='Select',
            ),
            html.Button(
                className='dropdown-button',
                children=['Select All'],
                id=ids.SELECT_ALL_PROBLEMS_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className='dropdown-button',
                children=['Select None'],
                id=ids.SELECT_NULL_PROBLEMS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
