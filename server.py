from datetime import timedelta

from flask import Flask

from data.data_handler import ScopedSession


# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)
server.config.update(SECRET_KEY='SOMETHING SECRET')  # TODO: store as environment variable: os.getenv("SECRET_KEY")
server.permanent_session_lifetime = timedelta(days=1)


@server.teardown_appcontext
def shutdown_session(exception=None):
    """
    Tear down the application context by removing the session.

    This function is called every time the application context tears down.
    It ensures that the session is removed, releasing any connection resources
    which were in use.

    :param exception: An exception object, if any.
    :type exception: Exception, optional
    """
    ScopedSession.remove()
