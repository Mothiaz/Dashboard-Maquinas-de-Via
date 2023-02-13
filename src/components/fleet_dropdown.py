import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from ..data.source import DataSource
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:

    all_fleets: list[str] = data[DataSchema.FLEET].tolist()
    unique_fleets: list[str] = sorted(set(all_fleets))

    @app.callback(
        Output(ids.FLEET_DROPDOWN, 'value'),
        [
            Input(ids.YEAR_DROPDOWN, 'value'),
            Input(ids.MONTH_DROPDOWN, 'value'),
            Input(ids.SELECT_ALL_FLEETS_BUTTON, 'n_clicks'),
            Input(ids.DATE_RANGE, 'start_date'),
            Input(ids.DATE_RANGE, 'end_date')
        ],
    )

    def select_all_fleets(years: list[str], months: list[str], _: int, start_date, end_date) -> list[str]:
        filtered_data = data.query('year in @years and month in @months and date >= @start_date and date <= @end_date')
        return sorted(set(filtered_data[DataSchema.FLEET].tolist()))

            # source.filter(
            # years= years,
            # months= months,
            # start_date=start_date,
            # end_date=end_date).unique_fleets

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
            ]
        )