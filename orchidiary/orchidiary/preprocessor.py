from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def user_info(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user:
                login(request, user)
            else:
                form.add_error("Wrong username or password")
    else:
        form = AuthenticationForm()
    
    return {'login_form':form}