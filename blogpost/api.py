from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from blogpost.models import Blogpost
from rest_framework import permissions


class BlogpsotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blogpost
        fields = ('title', 'author', 'body', 'slug')

class BlogpostSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = BlogpsotSerializer
    search_fields = 'title'

    def get_queryset(self):
        return Blogpost.objects.all()

    def list(self, request):
        queryset = Blogpost.objects.all()

        search_param = self.request.query_params.get('title', None)
        if search_param is not None:
            queryset = Blogpost.objects.filter(title__contains=search_param)

        serializer = BlogpsotSerializer(queryset, many=True)
        return Response(serializer.data)
