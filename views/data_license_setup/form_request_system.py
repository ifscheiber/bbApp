from dash import Dash, html, Input, Output, dcc, callback, page_container
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from views.data_license_setup.accordion_item_request_system import AccordionItemRequestSystem


import numpy as np
import pandas as pd
from datetime import date, datetime


class FormRequestSystem:

    def __init__(self, parent_page: str):

        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------

        self.tooltip_id = f'tooltip_add_new_data_license_{parent_page}'

        self.accordion_item_request_files = AccordionItemRequestSystem('request_files')
        self.accordion_item_response_files = AccordionItemRequestSystem('response_files')

        # --------------------------------------------------------------------------------------------------------------
        # Header of this sub-form
        # --------------------------------------------------------------------------------------------------------------
        header = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.H2('Request Systems',
                                className='lpn'),
                        width="auto",
                        class_name='lpn-row-no-padding-lr'
                    ),
                    dbc.Col(
                        html.I(
                            id=self.tooltip_id,
                            className='bi bi-question-circle lpn-tooltip'
                        ),
                        width="auto"
                    )
                ],
                align="center",
                className='lpn-row-no-padding-lr'
            ),
            className='lpn-form-header'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Accordion holding the different Request systems
        # --------------------------------------------------------------------------------------------------------------
        request_file_accordion = dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl(
                            "New Request System",
                            icon=DashIconify(
                                icon="bi:trash",
                                color='#6FB0B0',
                                width=20,
                            ),
                        ),
                        dmc.AccordionPanel(
                            self.accordion_item_request_files.visualization
                        ),
                    ],
                    value="customization",
                ),
                dmc.AccordionItem(
                    [
                        dmc.AccordionControl("Request System 2"),
                        dmc.AccordionPanel(
                            self.accordion_item_response_files.visualization
                        ),
                    ],
                    value="flexibility",
                ),
            ],
            chevronPosition='left',

        )


        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = dbc.Form(
            [
                dbc.Stack(
                    [
                        header,
                        dbc.Container(request_file_accordion, className='lpn-form-accordion')
                    ],
                    gap=3
                )
            ],
        )
