from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile, Skill
from django.db.models import Q


# /////////////////////////////////////////////////////////////////////////////////////////////////


def paginateProfiles(request, profiles, results):

    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # CUSTOM RANGE INDEX
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)


    return custom_range, profiles


#
def searchProfiles(request):
    # set search_query as an empty string to not mess up site if no input is placed
    search_query = ''
    #
    if request.GET.get('search_query'):
        # stores the value of search_query in html in a PY variable named search_query if the post method is a GET
        search_query = request.GET.get('search_query')
    # distinct() makes sure that a table/record is only returned once
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        # Show profiles where search_query == or icontains profile.skill.name
        Q(skill__name__icontains=search_query)
        )

    return profiles, search_query


