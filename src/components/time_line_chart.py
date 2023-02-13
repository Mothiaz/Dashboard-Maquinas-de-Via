import datetime

import pandas as pd
import plotly_express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from ..data.source import DataSource
from . import ids

# definir funcao que irá criar e atualizar o grafico

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.TIME_LINE_CHART, 'children'),
        [Input(ids.YEAR_DROPDOWN, 'value'),
         Input(ids.MONTH_DROPDOWN, 'value'),
         Input(ids.FLEET_DROPDOWN, 'value'),
         Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date')],
    )

    def update_bar_chart(
            years: list[str],
            months: list[str],
            fleets: list[str],
            start_date: str,
            end_date: str) -> html.Div:


        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        date_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days + 1)]
        pd_date_range = pd.DataFrame(date_range, columns=[DataSchema])
        pd_date_range[DataSchema.OM]=0
        filtered_data = data.query('date in '
                                   '@date_range')

        # filtered_data = data.query('date >= @start_date and date <= @end_date')


        if filtered_data.shape[0]==0:
            return html.Div('No data selected')

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(values=DataSchema.OM, index=DataSchema.DATE, aggfunc='count').reset_index()

            return pd.concat([pt, pd_date_range], axis=0).drop_duplicates(subset=DataSchema.DATE, keep='first').sort_values(by=DataSchema.DATE)

            # return pt.reset_index().sort_values(DataSchema.DATE)

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.')
        fig = px.line(
            create_pivot_table(),
            x=DataSchema.DATE,
            y=DataSchema.OM,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.TIME_LINE_CHART)
    return html.Div(id=ids.TIME_LINE_CHART)