from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
# GETS MODELS FILE FROM PROJECTS FORLDER AND IMPORTS "Project" CLASS
from projects.models import Project

from api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    # serializes data, turns it into json data
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # serializes data, turns it into json data
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def projectVote(request, pk):
#     project = Project.objects.get(id=pk)
#     user = request.user.profile
#     data = request.data

#     serializer = ProjectSerializer(project, many=False)
#     return Response(serializer.data)