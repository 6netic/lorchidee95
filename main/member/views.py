from django.contrib.auth import authenticate, login, logout
from . forms import ConnectForm, ChangePasswordForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User


def connect(request):
    """ Connects a user to the system """

    if request.method == 'POST':
        form = ConnectForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('planning:index'))
            else:
                error = True
    else:
        form = ConnectForm()
    return render(request, 'member/display_connect_page.html', locals())


def disconnect(request):
    """ Disconnects a user to the system """

    logout(request)
    form = ConnectForm()
    return render(request, "member/display_connect_page.html", locals())


def modify_password(request):
    """ Modifies user's password """

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                former_password = form.cleaned_data['old_password']
                new_password1 = form.cleaned_data['new_password1']
                new_password2 = form.cleaned_data['new_password2']
                if request.user.check_password(former_password):
                    if new_password2 == new_password1:
                        current_user = User.objects.get(username=request.user.username)
                        current_user.set_password(new_password2)
                        current_user.save()
                        return render(request, "member/display_modify_page.html", {'resp_ok': True})
                    else:
                        # Only former password is correct
                        resp = "only_former"
                else:
                    # Former password is false and new password is not the same in the two fields
                    resp = "none_of_them"
            except:
                # Data sent cannot be taken into account
                resp = "error_in_data"
            return render(request, "member/display_modify_page.html", locals())
    else:
        # First time form is loaded
        form = ChangePasswordForm()
        return render(request, "member/display_modify_page.html", {'form': form, 'resp': True})
