import pandas as pd
import plotly_express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
# from ..data.source import DataSource
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.FLEET_BAR_CHART, 'children'),
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
            start_date,
            end_date) -> html.Div:

        filtered_data = data.query('date >= @start_date and date <= @end_date and fleet in @fleets')
        # filtered_source = source.filter((years, months, fleets, start_date, end_date))

        if filtered_data.shape[0]==0:
            return html.Div('No data selected')

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.OM,
                index=[DataSchema.FLEET],
                aggfunc='count',
            )

            return pt.reset_index().sort_values(DataSchema.OM, ascending=False)

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.')

        fig = px.bar(
            create_pivot_table(),
            x=DataSchema.FLEET,
            y=DataSchema.OM,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.FLEET_BAR_CHART)
    return html.Div(id=ids.FLEET_BAR_CHART)