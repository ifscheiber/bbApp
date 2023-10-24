from flask import request, redirect, session, jsonify, url_for, render_template
from flask_login import login_user, logout_user, LoginManager, current_user

from dash import page_registry

from typing import Union

from server import server

from authentication import User, check_hash

from data.data_handler import ScopedSession

from data.models.user_orm import LeapNodeBillingUser


# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@server.route('/logout', methods=['GET'])
def logout():
    """
    Log out the current user and redirect to the login page.

    This endpoint handles the logout functionality. If the current user is authenticated,
    it logs out the user and then redirects to the login page.

    :return: Redirection to the login page.
    :rtype: werkzeug.wrappers.Response
    """

    if current_user.is_authenticated:
        logout_user()
        # TODO: Trigger a Note to the User on the Login Page telling about 'Successful Logout!'

    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id: str) -> Union[None, User]:
    """
    Load a user from the database based on the user_id.

    This function is used by the Flask-Login extension to load a user from the
    database, given the user_id. The user_id is the Unicode ID string for the user.

    :param user_id: The ID of the user to load from the database.
    :type user_id: str
    :return: An instance of the `LeapNodeBillingUser` object, or None if the user could not be found.
    :rtype: `LeapNodeBillingUser` or None

    :Example:

    user = load_user(user_id='1234')

    This will return the User object for the user with ID '1234', or None if no user with that ID exists.

    .. note:: This function requires a database session to query the database.
        It uses a scoped session from SQLAlchemy to handle the database connection.
    """
    db_session = ScopedSession()
    user = db_session.query(LeapNodeBillingUser).filter(LeapNodeBillingUser.id == user_id).first()

    if user:
        user = User(user.__dict__)

    return user


@server.before_request
def check_login():
    """
    Check the login status before processing a request.

    This function is executed before processing each request to ensure that the user is authenticated.
    For GET requests, it allows access to the login, logout, and assets paths without authentication.
    For other paths, it checks if the user is authenticated. If not, it stores the current URL in the session
    and redirects the user to the login page.
    For non-GET requests, it allows access to the login, recover_password, and notify paths, and checks for
    authentication for other paths. If the user is not authenticated, it returns a JSON response with a 401 status.

    :return: None if the user is authenticated or accessing allowed paths, otherwise a redirect to the login page
             or a JSON response with a 401 status.
    :rtype: None or werkzeug.wrappers.Response

    :Example:

    This function is used as a decorator for the Flask app instance, and does not need to be called directly.
    """
    if request.method == 'GET':
        if request.path in ['/login', '/logout'] or request.path.startswith('/assets/'):
            return
        if current_user:
            if current_user.is_authenticated:
                return
            else:
                for pg in page_registry:
                    if request.path == page_registry[pg]['path']:
                        session['url'] = request.url
        return redirect(url_for('login'))
    else:
        if current_user:
            if (request.path in ['/login', '/recover_password', '/notify']) or current_user.is_authenticated:
                return
        return jsonify({'status': '401', 'statusText': 'unauthorized access'})


@server.route('/login', methods=['POST', 'GET'])
def login(message: str = ""):
    """
    Handle user login functionality.

    This endpoint provides both GET and POST methods. The GET method renders the login page,
    while the POST method handles the login form submission. If the user provides valid
    credentials, they are logged in and redirected to the specified URL or the root URL.
    If the credentials are invalid, an error message is displayed.

    :type message: str
    :param message: An optional message to display on the login page, default is an empty string.
    :rtype: werkzeug.wrappers.Response
    :return: A response object, either rendering the login page or redirecting to another page.
    """
    redirect_url = '/'

    if request.method == 'POST' and request.form:
        email = request.form['email']
        password = request.form['password']
        hash_result, user = check_hash(email, password)

        if hash_result:
            login_user(User(user.__dict__))

            if 'url' in session and session['url']:
                redirect_url = session['url']
                session['url'] = None

            return redirect(redirect_url)

        else:
            message = "The username and/or password you entered was invalid. Please try again."

    elif current_user.is_authenticated:
        return redirect(redirect_url)

    return render_template('login.html', message=message)


@server.route('/recover_password', methods=['POST'])
def recover_password():
    # TODO: TO be implemented
    print('RECOVERED')
    email = request.json.get('email')

    # Handle password recovery logic here (e.g., send a recovery email)

    return jsonify(message="Recovery email sent!")


