import pandas as pd
import plotly_express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from ..data.source import DataSource
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.SYSTEM_BAR_CHART, 'children'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.SYSTEM_DROPDOWN, 'value'), ]
    )
    def update_bar_chart(
            start_date,
            end_date,
            systems: list[str],
    ) -> html.Div:

        filtered_data = data.query('date >= @start_date and date <= @end_date and system in @systems')

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected')

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.OM,
                index=[DataSchema.SYSTEM],
                aggfunc='count',
            )

            return pt.reset_index().sort_values(DataSchema.OM, ascending=False)

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.')
        fig = px.bar(
            create_pivot_table(),
            x=DataSchema.SYSTEM,
            y=DataSchema.OM,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.SYSTEM_BAR_CHART)

    return html.Div(id=ids.SYSTEM_BAR_CHART)
