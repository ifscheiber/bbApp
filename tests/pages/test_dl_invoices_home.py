from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

from views.data_license_setup.form_data_license import FormDataLicense

'''
This test module is for testing the functionality of the 'Home'-page (relative Path: '/'). 
The following functionalities are desired and need to be tested:

1. **DatePicker Menu:**
   a. Clicking the Calendar-Icon or the DatePicker-Input field should open the DatePicker Menu.
   b. When a Month is clicked in the DatePicker Menu, the DatePicker-Input field must be updated with this date.
   c. The Store.Component holding the dataframe for Tables and Figures must be updated accordingly upon date selection.
   d. Tables and/or Figures must be updated accordingly upon date selection.
   e. The update of the Table includes the update of the Snapshot Figure.

2. **Table Interaction:** 
    a. Clicking the 'bank account'-Icon in the Table should link the user to the 'Account Page' 
    with the associated 'Account ID'. 
    b. Clicking a Bar in the 'Snapshot Figure within the Table' should update the 
    DatePicker-Input field with the Date of this bar. c. All actions associated with the change of the input field must 
    be performed (update DatePickerInput, update data, update figures).

3. **Tab Selection:**
   a. Selecting another Tab should open the respective Tab and display its content.
   b. The default tab is 'Accounts'.

4. **Accounts Tab:** 
    a. Initially, all Select menus but the first one are deactivated. 
    b. Selecting a specific Request Type should activate the second Select Menu and update the figure to show the 
    breakdown of the selected request type costs into cost types. 
    c. Selecting a specific Cost Type should activate the next select menu for choosing the further drilldown into 
    Data Cat or Asset Types. 
    d. Changing the third select should update the Description on the fourth Select Menu, set it to 'All' if not, and 
    update the figure.
'''




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

