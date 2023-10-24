from dash import Dash, html, Input, Output, dcc, callback, page_container
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from views.dl_invoices.accordion_item_dl_invoices import AccordionItemDLInvoice

import numpy as np
import pandas as pd
from datetime import date, datetime


class AccordionDLInvoices:

    def __init__(self, parent_page: str):

        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------

        self.tooltip_id = f'tooltip_add_new_data_license_{parent_page}'
        self.header_account_id = f'header_account_{parent_page}'
        self.accordion_control_id = f'accordion_control_{parent_page}'
        self.accordion_panel_id = f'accordion_panel_{parent_page}'

        self.accordion_item_request_files = AccordionItemDLInvoice('request_files')
        self.accordion_item_response_files = AccordionItemDLInvoice('response_files')

        # --------------------------------------------------------------------------------------------------------------
        # Accordion holding the different Request systems
        # --------------------------------------------------------------------------------------------------------------
        accordion = dmc.Card(
            dbc.Stack(
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div("Invoice", className='lpn-form-sm-header'), className='col-auto'),

                        dbc.Col(
                            [DashIconify(icon='bi:filetype-xlsx', width=27, className='me-3'),
                            DashIconify(icon='bi:filetype-pdf', width=27)],
                            className='col lpn text-end'
                        ),



                    ]
                ),
                self.accordion_item_request_files.visualization
            ], gap=3
            )
        )


        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = dbc.Form(
            [
                dbc.Stack(
                    [
                        #header,
                        accordion
                    ],
                    gap=3
                )
            ],
        )
