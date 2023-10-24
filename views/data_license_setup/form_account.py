from dash import Dash, html, Input, Output, State, dcc, callback
from dash_framework.visualization_items.visualization_item import VisualizationItem
from dash_framework.components.tooltips import get_tooltip
import numpy as np
import pandas as pd
from datetime import date, datetime
import dash_bootstrap_components as dbc
from dash import html, dcc, page_registry, _pages, page_container
from dash_bootstrap_components import DropdownMenu, DropdownMenuItem
from views.data_license_setup.form_data_license import FormDataLicense
import dash_mantine_components as dmc


class FormAccount():

    def __init__(self, parent_page: str):
        """

        :type form_ids: list
        form_ids: contaons the ids of the individual input ids

        """
        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------
        self.input_account_number_id = f'input_account_number_{parent_page}'
        self.text_area_account_description_id = f'text_area_account_description_{parent_page}'
        self.date_picker_id = f'date_picker_{parent_page}'

        self.tooltip_id = f'tooltip_add_new_data_license_{parent_page}'
        self.tooltip_account_number_id = f'tooltip_invoice_dir_{parent_page}'
        self.tooltip_account_initialization_id = f'tooltip_usage_file_dir_{parent_page}'

        # --------------------------------------------------------------------------------------------------------------
        # Header of this sub-form
        # --------------------------------------------------------------------------------------------------------------
        header = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.H2('Account',
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
        # Input Account Number
        # --------------------------------------------------------------------------------------------------------------
        input_account_number = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_account_number_id,
                    placeholder="Enter Account Number",
                    disabled=False,
                    class_name='lpn-form-element-dark-mode lpn-margin-lr', ),
                dbc.Label("Account Number"),
                html.Div(
                    dbc.FormText('The path to the directory the monthly invoice packages are stored.'
                                 'For security, manually type or paste the directory path.',
                                 class_name='lpn-form-text'),
                    id=self.tooltip_account_number_id,
                    hidden=True)
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Input Account Description
        # --------------------------------------------------------------------------------------------------------------
        text_area_account_description = dbc.FormFloating(
            [
                dbc.Textarea(
                    id=self.text_area_account_description_id,
                    placeholder="Account Description",
                    disabled=False,
                    class_name='lpn-form-element-dark-mode lpn-margin-lr',

                ),
                dbc.Label("Description")
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Input Account Effective Date
        # --------------------------------------------------------------------------------------------------------------
        num_and_date = dbc.Container(
            dbc.Row(
            [
                dbc.Col(input_account_number, width=6, class_name='lpn-row-no-padding-lr'),
                dbc.Col(html.Div(
                    [
                        dcc.DatePickerSingle(
                            id='my-date-picker',
                            placeholder="",
                            style={'width': '100%'}
                        ),
                        html.I(className='bi bi-calendar-date datepicker-icon'),
                        dbc.Label('Initilization Date', class_name='datepicker-label')

                    ],
                    className='datepicker-container '
                ), width=6, class_name='lpn-datepicker-col')
            ],
            class_name='lpn-row-no-padding-lr'
        ),
            class_name='lpn-form-element-dark-mode')





        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = dbc.Form(
            dbc.Stack([
                header,
                num_and_date,
                text_area_account_description,
            ], gap=3)
        )



    def callbacks(self):
        pass
        '''@callback(
            Output(self.tooltip_account_number_id, 'hidden'),
            Output(self.tooltip_account_initialization_id, 'hidden'),
            Input(self.tooltip_id, 'n_clicks'),
            State(self.tooltip_account_number_id, 'hidden'),
            State(self.tooltip_account_initialization_id, 'hidden')
        )
        def toggle_tooltip(toggle_tooltips, hidden_account_number, hidden_account_initialization):
            return not hidden_account_number, not hidden_account_initialization'''
