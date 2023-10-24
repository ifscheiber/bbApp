from aiosmtpd.smtp import Envelope, Session
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message


class CustomSMTPHandler(Message):
    """
    CustomSMTPHandler class is an SMTP server implementation
    that prints incoming messages to the console.
    """

    async def handle_DATA(self, server, session: Session, envelope: Envelope):
        """
        Handles an incoming SMTP DATA command.

        This method will be invoked by the server when a client sends a DATA command.
        The server argument is the SMTP server instance that is calling this method.
        The session argument is an instance of Session which contains session-specific
        information about the SMTP session. The envelope argument is an instance of
        Envelope that contains the message from the client.

        :param server: SMTP server instance
        :type server: Controller
        :param session: Contains session-specific information
        :type session: Session
        :param envelope: Contains the message from the client
        :type envelope: Envelope

        :return: None
        :rtype: None
        """
        print(f'Receiving message from: {envelope.mail_from}')
        print(f'To: {", ".join(envelope.rcpt_tos)}')
        print(f'Message:\n{envelope.content.decode()}')

        return '250 Message accepted for delivery'

    def handle_message(self, message) -> None:
        print('ACTIVE')


def run():
    """
    Function to start the Custom SMTP Server. The server runs until
    the user presses a key, at which point the server is stopped and
    the function returns.

    :return: None
    :rtype: None
    """
    controller = Controller(CustomSMTPHandler(), hostname='localhost', port=1025)
    controller.start()

    print("SMTP server started. Press any key to stop the server...")
    input()
    print("Stopping server...")

    controller.stop()

    print("Server stopped.")


if __name__ == '__main__':
    run()