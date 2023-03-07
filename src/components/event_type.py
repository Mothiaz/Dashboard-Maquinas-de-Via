import pandas as pd
from dash import Dash, dcc, html

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_events: list[str] = data[DataSchema.EVENT].tolist()
    unique_events: list[str] = sorted(set(all_events))

    return html.Div(
        children=[
            html.H6('Event Type'),
            dcc.Checklist(
                id=ids.EVENT_TYPE,
                options=[{'label': event, 'value': event}
                         for event in unique_events],
                value=['']
            ),
        ]
    )
