from dash import Dash, html, Input, Output, State, dcc, callback, register_page
import dash_bootstrap_components as dbc

from datetime import datetime

from dl_billing.orm.client_setup.master_data import BBG_REF_CLIENTS

from data.data_handler import ScopedSession


class ClientSetupPage:

    def __init__(self, page_url: str = 'client-setup'):
        """

        :type form_ids: list
        form_ids: contaons the ids of the individual input ids

        """
        # --------------------------------------------------------------------------------------------------------------
        # IDs of the form
        # --------------------------------------------------------------------------------------------------------------
        # BBG_REF_CLIENTS IDs -->
        self.input_client_name_id = f'input_client_name_{page_url}_id'
        self.input_user_defined_client_id_id = f'input_user_defined_client_id_{page_url}_id'
        self.board_user_button_id = f'board_user_button_{page_url}_id'

        self.dl_billing_url_id = 'lpn_dl_billing_url_to_all_pages_id'

        # --------------------------------------------------------------------------------------------------------------
        # Input Client Name
        # --------------------------------------------------------------------------------------------------------------
        input_client_name = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_client_name_id,
                    placeholder="Enter Client Name",
                    disabled=False,
                    class_name='lpn-extra-margin-top-20px lpn-form-element-dark-mode'
                ),
                dbc.Label(
                    html.B("Client Name")
                )
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Input User Defined Client ID with Board New Client Button
        # --------------------------------------------------------------------------------------------------------------
        input_user_defined_client_id_id = dbc.FormFloating(
            [
                dbc.Input(
                    id=self.input_user_defined_client_id_id,
                    placeholder="Enter User Defined Client ID",
                    disabled=False,
                    type='number',
                    class_name='lpn-extra-margin-top-20px lpn-form-element-dark-mode mb-3'),
                dbc.Label(
                    html.B("User Defined Client ID")
                ),
                html.Button(
                    'Board Client',
                    id=self.board_user_button_id,
                    className='btn lpn-login-button'
                )
            ],
            class_name='lpn-form-element-dark-mode lpn-margin-lr'
        )

        # --------------------------------------------------------------------------------------------------------------
        # Assembled form
        # --------------------------------------------------------------------------------------------------------------
        form = dbc.Form(
            [input_client_name, input_user_defined_client_id_id], className='container'
        )

        self.visualization = html.Main(
            children=form,
            className='app-layout'
        )

    def define_callbacks(self):
        """
        Defines the dash.callbacks.
        Should consist of several inner functions, each specifying a callback.
        """
        pass
        @callback(
            Output(self.input_client_name_id, 'invalid'),
            Output(self.input_user_defined_client_id_id, 'invalid'),
            Input(self.board_user_button_id, 'n_clicks'),
            State(self.input_client_name_id, 'value'),
            State(self.input_user_defined_client_id_id, 'value'),
            prevent_initial_call=True
        )
        def board_client(board_user_button_n_clicks: int, client_name: str, ud_client: int):
            """
            TODO @Lennart: Why is ud_client type int? String would be more human understandable...

            TODO @ivo: Include duplicate checks for ud_client and client_name, in-line validation with out of focus!
                --> ClientSide - Callbacks!

            """

            # TODO @ivo Return dict here!

            if board_user_button_n_clicks:
                session = ScopedSession()

                new_client = BBG_REF_CLIENTS(
                    ud_client=ud_client,
                    client_name=client_name,
                    dt_effective=datetime.now(),
                    dt_termination=datetime.now()
                )

                session.add(new_client)
                session.commit()

            return False, False


# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
# create report
report = ClientSetupPage()


def layout():
    return report.visualization


# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='Board Client', path='/board-client', access_level=['admin'])
