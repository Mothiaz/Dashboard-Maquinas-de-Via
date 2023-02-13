import pandas as pd
from dash import Dash, html
# import pandas as pd

from ..data.source import DataSource
from src.components import (
    year_dropdown,
    month_dropdown,
    system_bar_chart,
    fleet_dropdown,
    fleet_bar_chart,
    time_line_chart,
    date_range,
)


# def create_layout (app: Dash) -> html.Div():
#     return html.Div(
#         className="app-div",
#         children=[
#             html.H1(app.title),
#             html.Hr(),
#             html.Div(
#                 className='dropdown_container', children=[nation_dropdown.render(app)]
#             ),
#             system_bar_chart.render(app, data)
#         ]
#     )


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div():
    return html.Div(
        className='app-div',
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    date_range.render(app, data),
                    fleet_dropdown.render(app, data),
                ]
            ),
            fleet_bar_chart.render(app, data),
            system_bar_chart.render(app, data),
            time_line_chart.render(app, data),
        ]
    )
