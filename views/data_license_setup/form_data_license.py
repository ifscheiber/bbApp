from dash import register_page, html, dcc, Output, State, Input, callback, callback_context, clientside_callback, \
    ClientsideFunction, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path


class FormDataLicense():

    def __init__(self, parent_page: str, directory: str = 'Invoice'):
        """

        :type form_ids: list
        form_ids: contaons the ids of the individual input ids

        """
        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------
        self.input_data_license_id = f'input_data_license_{parent_page}'
        self.input_invoice_dir_id = f'input_invoice_dir_{parent_page}'  # TODO: This may be selected vi a file opener
        self.input_usage_file_dir_id = f'usage_file_dir_{parent_page}'  # TODO: This may be selected vi a file opener

        self.tooltip_id = f'tooltip_add_new_data_license_{parent_page}'
        self.tooltip_invoice_dir_id = f'tooltip_invoice_dir_{parent_page}'
        self.tooltip_usage_file_dir_id = f'tooltip_usage_file_dir_{parent_page}'

        # --------------------------------------------------------------------------------------------------------------
        # Header of this sub-form
        # --------------------------------------------------------------------------------------------------------------
        header = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.H2('Data License',
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
        # Input Data License ID
        # --------------------------------------------------------------------------------------------------------------
        input_data_license = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_data_license_id,
                    placeholder="Enter Data License ID",
                    debounce=True,
                    class_name='lpn-form-element-dark-mode lpn-margin-lr',
                ),
                dbc.Label(
                    html.B("Data License ID")
                ),
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr lpn-extra-padding-bottom-12px'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Input Account Number
        # --------------------------------------------------------------------------------------------------------------
        input_fd_src = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_invoice_dir_id,
                    placeholder="Enter Directory Path",
                    debounce=True,
                    class_name='lpn-form-element-dark-mode'),
                dbc.Label(
                    html.B(f"Invoice Directory Path")
                ),
                html.Div(
                    dbc.FormText('The path to the directory the monthly invoice packages are stored.'
                                 'For security, manually type or paste the directory path.',
                                 class_name='lpn-form-text'),
                    id=self.tooltip_invoice_dir_id,
                    hidden=True)
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr lpn-extra-padding-bottom-12px'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Input Account Number
        # --------------------------------------------------------------------------------------------------------------
        input_uf_src = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_usage_file_dir_id,
                    placeholder="Enter Directory Path",
                    debounce=True,
                    class_name='lpn-form-element-dark-mode'),
                dbc.Label(
                    html.B(f"Usage File Directory Path")
                ),
                html.Div(
                    dbc.FormText('The path to the directory the monthly usage files are stored.'
                                 'For security, manually type or paste the directory path.',
                                 class_name='lpn-form-text'),
                    id=self.tooltip_usage_file_dir_id,
                    hidden=True)
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        self.visualization = dbc.Form(
            [
                dbc.Stack(
                    [
                        header,
                        input_data_license,
                        input_fd_src,
                        input_uf_src
                    ],
                    gap=3,
                ),
            ],
        )

    def callbacks(self, return_inner: bool = False):
        @callback(
            Output(self.tooltip_invoice_dir_id, 'hidden'),
            Output(self.tooltip_usage_file_dir_id, 'hidden'),
            Input(self.tooltip_id, 'n_clicks'),
            State(self.tooltip_invoice_dir_id, 'hidden'),
            State(self.tooltip_usage_file_dir_id, 'hidden'),
            prevent_initial_call=True
        )
        def toggle_tooltip(toggle_tooltips, hidden_invoice_dir, hidden_usage_file_dir):
            return not hidden_invoice_dir, not hidden_usage_file_dir

        @callback(

            Output(self.input_invoice_dir_id, 'valid'),
            Output(self.input_invoice_dir_id, 'invalid'),
            Input(self.input_invoice_dir_id, 'value'),
            prevent_initial_call=True
        )
        def validate_invoice_dir(path_str: str):

            dir_path = Path(path_str)

            outputs = dict(
                valid=no_update,
                invalid=no_update
            )

            if dir_path.exists() and dir_path.is_dir():
                outputs['valid'] = True
                outputs['invalid'] = False
            else:
                outputs['valid'] = False
                outputs['invalid'] = True

            return tuple(outputs.values())






        '''clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='large_params_function'
            ),
            Output('out-component', 'value'),
            Input('in-component1', 'value'),
            Input('in-component2', 'value')
        )'''

        if return_inner:
            return dict(
                toggle_tooltip=toggle_tooltip
            )
