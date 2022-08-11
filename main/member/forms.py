from django import forms


class ConnectForm(forms.Form):
    """ Creates a form to authenticate a user """

    username = forms.CharField(label="Utilisateur", widget=forms.TextInput)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    """ Creates a form to change user's password """

    old_password = forms.CharField(
        label="Entrez le mot de passe actuel: ", widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(
        label="Entrez le nouveau mot de passe: ", max_length=32, widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(
        label="Retapez le nouveau mot de passe: ", max_length=32, widget=forms.PasswordInput, required=True)