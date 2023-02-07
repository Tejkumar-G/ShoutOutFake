from django.core.serializers.json import Serializer
from rest_framework import serializers
from feeds import models


class ChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Challenge
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True)
    # commentsCount = len(comments.data)

    class Meta:
        model = models.Post
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    # report_to = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        # fields = '__all__'
        exclude = ['first_name', 'last_name', 'groups', 'user_permissions',
                   'date_joined', 'last_login']

    def validate(self, obj):
        obj['redeemPoint'] = 0
        obj['giveablePoint'] = 0
        obj['is_staff'] = False
        if obj['designation'].name == 'Manager':
            obj['is_superuser'] = True
            obj['is_staff'] = True
        return obj


class ChallengeMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChallengeMap
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id', 'likes')


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Designation
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    # posts = PostsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Tag
        fields = '__all__'


class ProductRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductReward
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = '__all__'


class SpecialRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpecialReward
        fields = '__all__'
