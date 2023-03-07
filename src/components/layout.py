import pandas as pd
from dash import Dash, html
# import pandas as pd

from src.components import (
    system_bar_chart,
    system_dropdown,
    fleet_dropdown,
    fleet_bar_chart,
    set_dropdown,
    time_line_chart,
    date_range,
    equipment_type,
    event_type,
)


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div():
    return html.Div(
        className='app-div',
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                children=[
                    date_range.render(app, data),
                    event_type.render(app, data),
                    html.Hr(),
                    equipment_type.render(app, data),
                    html.Hr(),
                    fleet_dropdown.render(app, data),
                    system_dropdown.render(app, data),
                    set_dropdown.render(app, data),
                ]
            ),
            html.Hr(),
            html.Div(
                className='graph-container',
                children=[
                    fleet_bar_chart.render(app, data),
                    system_bar_chart.render(app, data),
                    time_line_chart.render(app, data),
                ]
            ),
        ]
    )
