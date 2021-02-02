from rest_framework import serializers
from ..models import Subject, Course, Module, Content
from django.contrib.auth.models import User
from io import BytesIO

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'title', 'slug')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['name', 'description', 'order']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'owner', 'overview', 'created', 'modules']



#  Nested Serializers
class DiversedContent(serializers.RelatedField):
    
    def to_representation(self, value):
        # Calling The render method of content model
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    content = DiversedContent(read_only=True, many=False)
    class Meta:
        model = Content
        fields = ['content', 'order', 'id']


class SubjectTitleSerializer(serializers.RelatedField):

    def to_representation(self, value):
        return value.title


class ModuleSerializerWithContent(serializers.ModelSerializer):
    contents = ContentSerializer(read_only=True, many=True)
    class Meta:
        model = Module
        fields = ['name', 'description', 'order', 'contents']

class CourseSerializerWithmoduleAndContent(serializers.ModelSerializer):
    modules = ModuleSerializerWithContent(read_only=True, many=True)
    owner = serializers.StringRelatedField(many=False)
    subject = SubjectTitleSerializer(many=False, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'owner', 'overview', 'created', 'modules']

