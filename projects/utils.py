from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project
from django.db.models import Q


# /////////////////////////////////////////////////////////////////////////////////////////////////

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    # CUSTOM RANGE INDEX
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)

    return custom_range, projects


def searchProjects(request):
    # set search_query as an empty string to not mess up site if no input is placed
    search_query = ''
    #
    if request.GET.get('search_query'):
        # stores the value of search_query in html in a PY variable named search_query if the post method is a GET
        search_query = request.GET.get('search_query')
    # distinct() makes sure that a table/record is only returned once
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) |
        # Show projects where owner.name contains or == search_query input
        Q(owner__name__icontains=search_query) |
        # Show projects where tags.name contains or == search_query input
        Q(tags__name__icontains=search_query)
        )

    return projects, search_query


