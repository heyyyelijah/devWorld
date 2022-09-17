from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .utils import searchProjects, paginateProjects
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from .models import Project,Tag


# /////////////////////////////////////////////////////////////////////////////////////////////////


def projects(request):
    projects, search_query = searchProjects(request)
    # 
    custom_range, projects = paginateProjects(request, projects, 9)
    # 
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    # renders projects.html with context
    return render(request, 'projects/projects.html', context)



def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        # saves review to the current project object where id=pk
        review.project = projectObj
        # saves the owner of the review as the currently signed in user profile
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'review successfully submitted')

        # update vote count

        return redirect('project', pk=projectObj.id)

    context = {'project': projectObj, 'form': form,}
    # renders single-project.html and passes in pk as an object to be used within the html file
    return render(request, 'projects/single-project.html', context)

#
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        # gets each tag from FORM then splits the words, then stored into a list.
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        # request.FILES adds files to the form
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # gets the instance of project
            project = form.save(commit=False)
            # updates the owner of the project model as the current profile
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        # gets each tag from FORM then splits the words, then stored into a list.
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        # 
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    # 
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    # 
    context = {'object':project}
    return render(request, 'delete_template.html', context)