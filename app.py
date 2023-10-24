from flask_login import current_user

from dash import Dash, page_container, page_registry, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc

from dash_framework.page_layouts.navbars import get_lpn_app_navbar
from dash_framework.page_layouts.footers import get_footer

from server import server

# NOTE: The import of the login module is necessary for login functionality
# Removing the import of the login module will make the app inaccessible!
from authentication import login

import atexit

# ----------------------------------------------------------------------------------------------------------------------
# Version-specific url-parts
# ----------------------------------------------------------------------------------------------------------------------
# TODO: May be added ...

# App Settings
app = Dash(__name__,
           server=server,
           use_pages=True,
           suppress_callback_exceptions=True,
           external_stylesheets=[
               dbc.themes.BOOTSTRAP,
               dbc.icons.BOOTSTRAP
           ],# TODO: Better download!
           external_scripts=[
               {'src': "https://cdn.plot.ly/plotly-2.26.0.min.js"}
               # TODO: You may download the js on 'https://plotly.com/javascript/getting-started/'
           ]

           )

links = [(page["name"], page["relative_path"]) for page in page_registry.values()]

# App IDs
dl_billing_url_id = 'lpn_dl_billing_url_to_all_pages_id'


# App Layout
def layout():
    return html.Div(
        [
            dcc.Location(
                id=dl_billing_url_id
            ),
            get_lpn_app_navbar(
                links=links[1:4],
                current_user=current_user
            ),
            html.Div(
                page_container,
                className='dash-app-content'
            ),
            get_footer(),
        ],
        id='DashLayoutNavbar',
        className='app-layout'
    )


# To alter navbar links the layout must be a function:
# https://community.plotly.com/t/dash-app-pages-with-flask-login-flow-using-flask/69507/52
# TODO: THe access_level attribute must also be checked when trying to load the page to Enable ROLE PERMISSION
#   --> check how to do that!
app.layout = layout


# Clean Up
def cleanup_on_shut_down():
    """
    Perform cleanup operations when the application is shutting down.

    .. warning::
       This method is designed to be used with the `atexit` module in a standalone
       Flask/Dash application. If the app is running in a WSGI server like Gunicorn
       or uWSGI, this method might not be called during the server's shutdown process.
       In such cases, server-specific hooks should be used to ensure proper cleanup.
    """
    # TODO: Every User has to logout

    # If in Debugging Mode -> Do Nothing
    if app._hot_reload:
        return

    login.logout() #TODO must be in a forloop

    print("Cleaning up...")


# Register function that will be triggered on shutdown of the LOCAL servers!
atexit.register(cleanup_on_shut_down)

# ----------------------------------------------------------------------------------------------------------------------
# App Main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    app.run_server(
        debug=True,
    )
