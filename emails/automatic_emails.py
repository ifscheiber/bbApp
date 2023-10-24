from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
import smtplib
from abc import abstractmethod


class AutomaticEmail:
    def __init__(self,
                 subject: str,
                 sender: str,
                 recipients: list,
                 cc: list = None,
                 smtp_server=None,  # TODO: which server to use?
                 ):
        """

        :param subject: The subject of the email
        :param sender: The sender's email address.
        :param recipients: A list of receiver email-addresses
        :param cc: A list of receiver email-addresses in cc
        :param smtp_server: The email-server  # TODO: which server to use?
        """
        self.smtp_server = smtp_server
        # --------------------------------------------------------------------------------------------------------------
        # Add EMail Header
        # --------------------------------------------------------------------------------------------------------------
        self.message = EmailMessage()
        self.message['subject'] = subject
        self.message['From'] = self.parse_email_address(sender)
        self.message['To'] = [self.parse_email_address(recipient) for recipient in recipients]
        if cc:
            self.message['Cc'] = [self.parse_email_address(recipient) for recipient in cc]
        # --------------------------------------------------------------------------------------------------------------
        # Default internal CSS
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Think about it
        self.style = """
            header {
                font-family: "Arial;
                font-size: "10pt"
            }
            
            body {
                font-family: "Arial;
                font-size: "10pt";
                color: #000000
            }
            
            .address {
                font-family: "Arial;
                font-size: "10pt"
            }
        """
        # --------------------------------------------------------------------------------------------------------------
        # EMail-Signature
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Think about it
        sender_signature_name = 'LeapNode'
        self.logo = make_msgid()
        self.signature = """
        <hr style="height: 1px; border-width: 0; background-color: #111111">
        <p class = address>
            {name}
            <br>
            <img src="cid:{logo}" width="auto"/>
        </p>
        """.format(
            name=sender_signature_name,
            logo=self.logo[1:-1]
        )

    def add_content(self):
        """
        Add content to message
        """
        self.message.set_content(
            self.define_text_content()
        )
        self.message.add_alternative(
            self.define_html_content(),
            subtype='html'
        )
        # TODO Enable to attatch logo
        # with open('logo.png', 'rb') as img:
        #    self.message.get_payload()[1].add_related(img.read(), 'image', 'png', cid=self.logo)

    def add_attachments(self, attachments: list):
        """

        :param attachments:
        """
        for attachment in attachments:
            if '/' in attachment:
                file_name = attachment.split('/')[1]
            else:
                file_name = attachment
            with open(attachment, 'rb') as fp:
                file_data = fp.read()
            self.message.add_attachment(
                file_data,
                main_type='application',
                subtype='octet-stream',
                file_name=file_name
            )

    @staticmethod
    def parse_email_address(email_address: str):
        """
        Creates an Address-object from the email-address supplied.

        :param email_address: The email-address to be parsed
        """
        display_name = email_address.lower().split('@')[0].split('.')
        if len(display_name) == 2:
            display_name = display_name[1].capitalize() + ',' + display_name[0].capitalize()
        else:
            display_name = display_name[0]
        address = Address(
            display_name=display_name,
            addr_spec=email_address
        )
        return address

    def send_email(self):
        """
        Sends the message as an email to the message receivers.
        """
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(self.message)

    @abstractmethod
    def define_text_content(self) -> str:
        """
        Defines the text-content of the email.

        :return: The text content to be displayed in the email.
        """
        pass

    @abstractmethod
    def define_html_content(self) -> str:
        """
        Defines the html-content of the email.

        :return: The html content to be displayed in the email.
        """
        pass


class WelcomeNewUserEmail(AutomaticEmail):
    def __init__(self,
                 sender: str,
                 recipient: str,
                 user_id: str,
                 initial_password: str,
                 smtp_server=None,
                 attachments: list = None
                 ):
        self.subject = "Registration LeapNode"
        AutomaticEmail.__init__(
            self,
            subject=self.subject,
            sender=sender,
            smtp_server=smtp_server,
            recipients=[recipient]
        )
        self.user_id = user_id
        self.initial_password = initial_password
        # --------------------------------------------------------------------------------------------------------------
        # EMail content
        # --------------------------------------------------------------------------------------------------------------
        self.add_content()
        if attachments:
            self.add_attachments(attachments)

    def define_text_content(self) -> str:
        """
        Defines the text-content of the email.

        :return: The text content to be displayed in the email.
        """
        text = f"Dear {self.user_id},\n\n" \
               f"Thank you for registering. " \
               f"Your may log in with the following credentials:\n\n" \
               f"user_id: {self.user_id}\n" \
               f"password: {self.initial_password}\n\n " \
               f"For security reasons change the initial password " \
               f"provided above as soon as possible.\n\n" \
               f"Kind Regards\n" \
               f"The LeapNode-Team"
        return text

    def define_html_content(self) -> str:
        """
        Defines the html-content of the email.

        :return: The html content to be displayed in the email.
        """
        html_content = "Some html content"
        return html_content


class ResetPasswordLinkEmail(AutomaticEmail):
    def __init__(self,
                 sender: str,
                 recipient: str,
                 user_id: str,
                 url: str,
                 smtp_server=None,
                 attachments: list = None
                 ):
        self.subject = "Registration MitoAnn"
        AutomaticEmail.__init__(
            self,
            subject=self.subject,
            sender=sender,
            smtp_server=smtp_server,
            recipients=[recipient]
        )
        self.user_id = user_id
        self.url = url
        # --------------------------------------------------------------------------------------------------------------
        # EMail content
        # --------------------------------------------------------------------------------------------------------------
        self.add_content()
        if attachments:
            self.add_attachments(attachments)

    def define_text_content(self) -> str:
        """
        Defines the text-content of the email.

        :return: The text content to be displayed in the email.
        """
        text_content = f"Dear {self.user_id}\n\n," \
                       f"You requested a password reset. " \
                       f"To reset your password please follow the link below:\n\n" \
                       f"{self.url}"
        return text_content

    def define_html_content(self) -> str:
        """
        Defines the html-content of the email.

        :return: The html content to be displayed in the email.
        """
        html_content = f"Dear {self.user_id}\n\n," \
                       f"You requested a password reset. " \
                       f"To reset your password please follow the link below:\n\n" \
                       f"{self.url}"
        return html_content

