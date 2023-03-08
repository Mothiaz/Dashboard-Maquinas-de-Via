import pandas as pd
import plotly_express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.SET_BAR_CHART, 'children'),
        [Input(ids.DATE_RANGE, 'start_date'),
         Input(ids.DATE_RANGE, 'end_date'),
         Input(ids.EQUIPMENT_DROPDOWN, 'value'),
         Input(ids.SET_DROPDOWN, 'value'),
         Input(ids.EVENT_TYPE, 'value')]
    )
    def update_bar_chart(start_date, end_date,
                         equips: list[str], conjuntos: list[str],
                         event: list[str]) -> html.Div:

        filtered_data = data.query('date >= @start_date and date <= @end_date '
                                   'and equip in @equips and conjunto in @conjuntos '
                                   'and event in @event')

        if filtered_data.shape[0] == 0:
            return html.Div('No data selected.')

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.OM,
                index=[DataSchema.SET],
                aggfunc='count',
            )

            return pt.reset_index().sort_values(DataSchema.OM, ascending=False)

        fig = px.bar(
            create_pivot_table(),
            x=DataSchema.SET,
            y=DataSchema.OM,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.SET_BAR_CHART)

    return html.Div(id=ids.SET_BAR_CHART)
