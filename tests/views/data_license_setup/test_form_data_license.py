from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

from views.data_license_setup.form_data_license import FormDataLicense


class TestToggleTooltip:
    """
    Test cases for the `toggle_tooltip` callback functionality within the :class:`FormDataLicense` class.
    """

    @staticmethod
    def toggle_tooltip():
        """
        Retrieve the inner :func:`~FormDataLicense.callbacks.toggle_tooltip` function
        from the :class:`FormDataLicense` class. This function is a callback that toggles
        the visibility of tooltips for invoice and usage file directories based on user interactions.

        :return: The inner `toggle_tooltip` callback function.
        :rtype: function
        """
        return FormDataLicense('test').callbacks(return_inner=True)['toggle_tooltip']

    def test_toggle_tooltip_show(self):
        """
        Test the behavior of :func:`~FormDataLicense.callbacks.toggle_tooltip` when the
        tooltips should be shown.
        """
        output = self.toggle_tooltip()(1, True, True)
        assert output == (False, False)

    def test_toggle_tooltip_hide(self):
        """
        Test the behavior of :func:`~FormDataLicense.callbacks.toggle_tooltip` when the
        tooltips should be hidden.
        """
        output = self.toggle_tooltip()(1, False, False)
        assert output == (True, True)

