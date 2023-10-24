from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from datetime import datetime


class Header2Row:

    def __init__(self, parent_page: str):

        self.datepicker_id = f"date_picker_{parent_page}_id"
        self.total_billed_amount_id = f"total_billed_amount_{parent_page}_id"

        billing_period = dbc.Stack(
            [
                html.Div('Billing Month', className='lpn-form-sm-header'),
                dmc.DatePicker(
                    placeholder='Select a Date',
                    id=self.datepicker_id,
                    clearable=False,
                    value=datetime.now().date(),
                    icon=DashIconify(
                        icon="bi:calendar",
                        width=16
                    ),
                    className='lpn-form-sm',
                ),
            ], gap=2
        )

        total_billed = dbc.Stack(
            [
                html.Div(
                    "Total Billed Amount",
                    className='lpn-form-sm-header'
                ),
                html.Div(
                    id=self.total_billed_amount_id,
                    className='lpn-number-big-2 margin-left-24px'
                ),
            ],
            gap=2
        )

        self.content = dbc.Row(
            [
                dbc.Col(
                    billing_period,
                    class_name='col-auto me-5'
                ),
                dbc.Col(
                    total_billed,
                    class_name='col text-end'
                )
            ],
            className='mb-5'
        )