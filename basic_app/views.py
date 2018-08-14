from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice!')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            # This is about "PASSWORD_HASHERS" item defined within settings.py
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  # OneToOne relationship user = models.OneToOneField(User) models.py

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                            {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered,})

def user_login(request):

    if request.method == 'POST':
        # username and password comes from login.html name value for both name and passwd
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('Account not Active')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and password: {}'.format(username, password))
            return HttpResponse('Invalid login details supplied!')
    else:
        print('something got wrong')
        return render(request, 'basic_app/login.html', {})
