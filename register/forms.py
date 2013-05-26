'''
by fmy 2013 based on Lion's code
'''
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django import forms
from horizon.utils import validators
from django.conf import settings
from django.views.decorators.debug import sensitive_variables
import ConfigParser
import commands
"""
Forms used for Horizon's register mechanisms.
"""
class RegForm(forms.Form):
    """ Form used for logging in a user.

    Handles authentication with Keystone, choosing a tenant, and fetching
    a scoped token token for that tenant. Redirects to the URL returned
    by :meth:`horizon.get_user_home` if successful.

    Subclass of :class:`~forms.Form`.
    """
    
    username = forms.CharField(label=_("User Name"), min_length=5, max_length=30, required=True)
    password = forms.RegexField(
            label=_("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            error_messages={'invalid': validators.password_validator_msg()})
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
    def clean(self):
        password = self.cleaned_data.get('password', '').strip()
        return self.cleaned_data

