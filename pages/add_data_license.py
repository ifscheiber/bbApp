from dash import callback, Output, Input, State, callback_context, register_page, html

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from dash_iconify import DashIconify

from views import FormDataLicense, FormAccount, FormRequestSystem




min_step = 0
max_step = 4
active = 0


def get_icon(icon):
    return DashIconify(icon=icon, height=20)


class FormAddDataLicense:
    def __init__(self):
        self.data_license_form = FormDataLicense('add_data_license_data_license')
        self.account_form = FormAccount('add_data_license_account')


        set_request_systems = FormRequestSystem('dl_setup_add_request_system')


        stepper = dbc.Container(
            [   (html.H1('Add Data License', className='lpn stepper-form600px')),
                dmc.Stepper(
                    id="stepper-custom-icons",
                    active=active,
                    breakpoint="sm",
                    size='sm',

                    style={'width': '80%', 'max-width': '80%', 'margin': 'auto'},
                    children=[
                        dmc.StepperStep(
                            label="Data License",
                            #description="Configure Directory",
                            icon=get_icon(icon="mdi:receipt-text-outline"),
                            progressIcon=get_icon(icon="mdi:receipt-text-outline"),
                            completedIcon=get_icon(
                                icon="mdi:receipt-text-check-outline"
                            ),
                            children=[

                                self.data_license_form.visualization
                            ]
                        ),

                        dmc.StepperStep(
                            label="Account",
                            #description="Define account",
                            icon=get_icon(icon="mdi:bank"),
                            progressIcon=get_icon(icon="mdi:bank"),
                            completedIcon=get_icon(icon="mdi:bank-check"),
                            children=[
                                self.account_form.visualization
                            ],
                        ),

                        dmc.StepperStep(
                            label="Request System",
                            #description="Get full access",
                            icon=get_icon(icon="tabler:device-desktop"),
                            progressIcon=get_icon(icon="tabler:device-desktop"),
                            completedIcon=get_icon(icon="tabler:device-desktop-check"),
                            children=[
                                set_request_systems.visualization
                            ],
                        ),

                        dmc.StepperCompleted(
                            children=[
                                dmc.Text(
                                    "Completed, click back button to get to previous step",
                                    align="center",
                                )
                            ]
                        ),
                    ],
                ),
                dbc.Row(
                    children=[
                        dbc.Col(dbc.Button(id="back-custom-icons", class_name='bi bi-chevron-left lpn-button-centered lpn-stepper-previous-btn'),
                                class_name='lpn-row-no-padding-lr', width=6),
                        dbc.Col(dbc.Button(id="next-custom-icons", class_name='bi bi-chevron-right lpn-button-centered lpn-stepper-next-btn'),
                                class_name='lpn-row-no-padding-lr', width=6),
                    ], className='lpn-stepper-form-row lpn-row-no-padding-lr'
                ),
            ],


        )

        self.visualization = html.Main(stepper, className='app-layout', )

    def define_callbacks(self):

        self.data_license_form.callbacks()
        self.account_form.callbacks()

        @callback(
            Output("stepper-custom-icons", "active"),
            Input("back-custom-icons", "n_clicks"),
            Input("next-custom-icons", "n_clicks"),
            State("stepper-custom-icons", "active"),
            prevent_initial_call=True,
        )
        def update_with_icons(back, next_, current):
            button_id = callback_context.triggered_id
            step = current if current is not None else active
            if button_id == "back-custom-icons":
                step = step - 1 if step > min_step else step
            else:
                step = step + 1 if step < max_step else step
            return step


# ----------------------------------------------------------------------------------------------------------------------
# Register Page
# ----------------------------------------------------------------------------------------------------------------------
report = FormAddDataLicense()


def layout():
    return report.visualization


# include callbacks
report.define_callbacks()

# register page
register_page(__name__, name='New Account', path='/add-data-license')
