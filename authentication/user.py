from flask_login import UserMixin
from data.models.user_orm import LeapNodeBillingUser


class User(LeapNodeBillingUser, UserMixin):

    def __init__(self, existing_user: dict):
        """
        Initialize a new User object by updating the existing user dictionary and calling the parent class constructors.

        This method initializes a new User object by removing the '_sa_instance_state' key from the existing_user
        dictionary (if present) and then calling the parent class constructors with the updated dictionary.

        :param existing_user: A dictionary containing the details of an existing user.
        :type existing_user: dict

        :raises KeyError: If the '_sa_instance_state' key is not present in the existing_user dictionary.

        :Inherited from LeapNodeBillingUser:
            - `id`: Unique identifier for each LeapNodeUser.
            - `role`: The User's Role, i.e., access level.
            - Other attributes inherited from `LeapNodeUser` class.

        :Inherited from UserMixin:
            - `is_active()`: Returns the status of the user.
            - `get_id()`: Returns the user_id.
            - `is_authenticated()`: Always returns True as all users are authenticated.
            - `is_anonymous()`: Always returns False as anonymous users are not allowed.
        """
        try:
            existing_user.pop('_sa_instance_state')
        except KeyError:
            pass

        super(User, self).__init__(**existing_user)

    def is_active(self):
        return self.status

    def get_id(self):
        """
        Return the user_id
        """
        return self.id

    def is_authenticated(self):
        """
        True, as all users are authenticated
        """
        return True

    def is_anonymous(self):
        """
        False, as anonymous users are not allowed
        """
        return False

    def get_role(self):
        """
        :return: Role of the user
        """
        return self.role
