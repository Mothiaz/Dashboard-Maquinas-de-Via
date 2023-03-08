import pandas as pd
from dash import Dash, html
import dash_bootstrap_components as dbc

from src.components import (
    system_bar_chart, system_dropdown,
    fleet_dropdown, fleet_bar_chart,
    equipment_dropdown, equipment_bar_chart,
    set_dropdown, set_bar_chart,
    item_dropdown, item_bar_chart,
    problem_dropdown, problem_bar_chart,

    time_line_chart,
    date_range,
    equipment_type,
    event_type,
)


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div():
    return dbc.Container(
        className='dbc',
        children=[
            html.H1(app.title, style={'textAlign': 'center'}),
            html.Hr(),
            html.Div(
                children=[
                    date_range.render(app, data)
                ]
            ),
            html.Div(
                children=[
                    event_type.render(app, data),
                    equipment_type.render(app, data),
                ]
            ),
            html.Div(
                children=[
                    fleet_dropdown.render(app, data),
                    equipment_dropdown.render(app, data),
                    system_dropdown.render(app, data),
                    set_dropdown.render(app, data),
                    item_dropdown.render(app, data),
                    problem_dropdown.render(app, data),
                ]
            ),
            html.Hr(),
            html.Div(
                children=[
                    fleet_bar_chart.render(app, data),
                    equipment_bar_chart.render(app, data),
                    system_bar_chart.render(app, data),
                    set_bar_chart.render(app, data),
                    item_bar_chart.render(app, data),
                    problem_bar_chart.render(app, data),
                    time_line_chart.render(app, data),
                ]
            ),
        ]
    )
