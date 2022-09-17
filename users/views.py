from .forms import CustomUserCreationForm, ProfileForm, SkillsForm, MessageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Profile, Message
from django.contrib import messages
from django.conf import settings


# Create your views here.


def loginUser(request):
    page = 'login'
    # 
    if request.user.is_authenticated:
        return redirect('profiles')
    # 
    if request.method == 'POST':
        usernameInput = request.POST['username'].lower()
        passwordInput = request.POST['password']
        try:
            # check if there is a user with the same username as inputted
            user = User.objects.get(username=usernameInput)    
        except:
            messages.error(request, 'Username does not exist')
        # RETURNS AN INSTANCE IF USER IS FOUND, ELSE NONE IS RETURNED
        user = authenticate(request, username=usernameInput, password=passwordInput)
        # 
        if user is not None:
            # will create a session for the user in the database, and will add the session to browser's cookies
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'username or password is incorrect')
    ###
    return render(request, 'users/login_register.html')


def logoutUser(request):
    # deletes session
    logout(request)
    messages.info(request, 'User logged out successfully')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    ###
    if request.method == 'POST':
        # ///
        form = CustomUserCreationForm(request.POST)
        # checks if form is valid
        if form.is_valid():
            # get an instance of user
            user = form.save(commit=False)
            # saves username as all lowercase in the database to avoid same name but different capitalizations
            user.username = user.username.lower()
            user.save()
            # creates alert that user was creted
            messages.success(request, 'User account was created')

            login(request, user)

            subject = 'welcome to devWorld'
            message_body = 'Glad to have you on board!'

            # send welcome message through email
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                ['zjgaray@gmail.com'],
                fail_silently=False,

            )

            return redirect('edit-account')
        else:
            messages.error(request, 'An error has ocurred during registration.')
    ###
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)



def profiles(request):

    # store in variables the search_queries from a diff py file
    profiles, search_query = searchProfiles(request)
    #####
    custom_range, profiles = paginateProfiles(request, profiles, 9)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


def userProfiles(request, pk):
    profile = Profile.objects.get(id=pk)
    user = profile.user

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills, 'user': user}
    return render(request, 'users/user-profile.html', context)


# RENDERS PAGE FOR PERSONAL ACCOUNT IF LOGGED IN, FOR EDITING AND ETC
@login_required(login_url="login")
def userAccount(request):
    # get am instance of the current logged in user's profile.
    profile = request.user.profile
    # gets a queryset of all skills of current logged in user
    skills = profile.skill_set.all()
    # gets a queryset of all projects of current logged in user
    projects = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    # pass to a var a model form from users/forms.py
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillsForm()

    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added successfully')
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    currentSkill = instance=profile.skill_set.get(id=pk)
    form = SkillsForm(instance=currentSkill)

    if request.method == 'POST':
        form = SkillsForm(request.POST, instance=currentSkill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully')
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    currentSkill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        # DELETE SKILL WHERE ID == PK
        currentSkill.delete()
        messages.success(request, 'Skill updated successfully')
        return redirect('account')
    ###
    context = {'object':currentSkill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # filters and gets the messages of the current user.
    userMessages = profile.messages.all()
    # counts the total length of unread messages
    newMessagesLen = userMessages.filter(is_read=False).count()

    context = {'userMessages':userMessages,'newMessagesLen':newMessagesLen}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def message(request, pk):
    profile = request.user.profile
    # Makes sure not to be able to view messages of others if they get a hold of UUID of 
    # other recipient's message/s
    if profile == Message.objects.get(id=pk).recipient:
        message = Message.objects.get(id=pk)
        message.is_read = True
        message.save()
    # redirect them to their inbox if they are trying to access a message they do not own
    else:
        return redirect('inbox')
    ###
    context = {'message':message,}
    return render(request, 'users/message.html', context)


def sendMessage(request, pk):
    recipient_profile = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.method == 'POST':
        # GET FORM INSTANCE
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            # IF SENDER OF MESSAGE IS NOT SIGNED IN
            if request.user == 'AnonymousUser':
                message.name = request.POST()['name']
                message.email = request.POST()['email']
            # IF CURRENT USER IS SIGNED IN
            elif request.user.is_authenticated:
                message.sender = request.user.profile
                message.name = request.user.profile.name
                message.email =  request.user.profile.email
            message.recipient = recipient_profile
            
            # SAVE MESSAGE IF DONE
            message.save()
            messages.success(request, 'Message was sent')
            return redirect('user-profile', pk=pk)

        
    context = {'form':form, 'recipient_profile': recipient_profile}
    return render(request, 'users/message_form.html', context)