import json

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from feeds.api.permissions import (
    IsAdminOrReadonly,
    IsIndividualUser,
    AcceptOrDeclineChallengeIfSameUser
)
from feeds.models import (
    Challenge,
    Post,
    ProductReward,
    Tag,
    User,
    Designation,
    Role,
    Comment,
    Resource,
    ChallengeMap,
    ProductCategory,
)
from .serializers import (
    ChallengesSerializer,
    PostsSerializer,
    ProductRewardSerializer,
    ProductCategorySerializer,
    TagsSerializer,
    UsersSerializer,
    DesignationSerializer,
    RoleSerializer,
    PostLikeSerializer,
    CommentSerializer,
    ResourceSerializer,
    ChallengeMapSerializer,
)


def get_required_response(data={}, records=[], message=''):
    response_data = dict(data=data, records=records, message=message)
    return response_data


class ChallengesList(generics.ListCreateAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengesSerializer


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengesSerializer


class ResourcesList(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class UsersList(APIView):
    permission_classes = [IsAdminOrReadonly, ]

    def get(self, request):
        users = User.objects.prefetch_related('reporter').all()
        serializer = UsersSerializer(users, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):

        serializer = UsersSerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChallengeMapList(APIView):
    permission_classes = [IsIndividualUser, ]

    def get(self, request):
        challenge_maps = ChallengeMap.objects.all()
        serializer = ChallengeMapSerializer(challenge_maps, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        # request.data['creatorId'] = request.user.uid
        serializer = ChallengeMapSerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChallengeMapDetail(generics.UpdateAPIView):
    queryset = ChallengeMap.objects.all()
    serializer_class = ChallengeMapSerializer
    permission_classes = [AcceptOrDeclineChallengeIfSameUser]

    # def update(self, request, *args, **kwargs):
    #
    #     serializer = ChallengeMapSerializer(challenge_map, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsList(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        print(request.data)
        serializer = TagsSerializer(data=request.data['data'])

        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class DesignationsList(APIView):

    def get(self, request):
        tags = Designation.objects.all()
        serializer = DesignationSerializer(tags, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        print(request.data)
        serializer = DesignationSerializer(data=request.data['data'])

        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class RolesList(APIView):

    def get(self, request):
        tags = Role.objects.all()
        serializer = RoleSerializer(tags, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        print(request.data)
        serializer = RoleSerializer(data=request.data['data'])

        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class CreatePost(APIView):
    permission_classes = [IsIndividualUser, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        print(request.data)
        serializer = PostsSerializer(data=request.data['data'])

        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class EditPost(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsIndividualUser, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

    # def get(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = PostsSerializer(post)
    #     return Response(serializer.data)

    # def put(self, request, pk=None):
    #     post = Post.objects.get(pk=pk)
    #     self.check_object_permissions(request, post)
    #     if post.fromId != request.user.uid:
    #         return Response({'detail': 'You can not edit this Post'})
    #     serializer = PostsSerializer(post, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)

    # def delete(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeDetails(APIView):
    permission_classes = [IsIndividualUser, ]
    authentication_classes = [TokenAuthentication, ]

    def put(self, request, pk=None):
        post_id = request.query_params.get('postId', None)
        user_id = request.query_params.get('userId', None)
        print(f'{post_id} {user_id}')
        if post_id and user_id:
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

            # user = User.objects.get(pk=user_id)
            if user_id in post.likes:
                return Response({"error": "User already the post"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                post.likes.append(user_id)
                post.save()
                return Response({"likes": post.likes})
        else:
            return Response({"error": "Invalid URL"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostLikeSerializer(post)
        return Response(get_required_response(data=serializer.data))


class CreateProductCategory(APIView):

    def get(self, request):
        product_category = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(product_category, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class CreateProductReview(APIView):

    def get(self, request):
        product_reward = ProductReward.objects.all()
        serializer = ProductRewardSerializer(product_reward, many=True)
        return Response(get_required_response(records=serializer.data))

    def post(self, request):
        serializer = ProductRewardSerializer(data=request.data['data'])
        if serializer.is_valid():
            serializer.save()
            return Response(get_required_response(data=serializer.data))
        else:
            return Response(serializer.errors)


class PostCommentsList(APIView):
    permission_classes = [IsIndividualUser, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None):
        try:
            comments = Comment.objects.filter(parentCreatorId=pk)
        except Post.DoesNotExist:
            return Response({'Error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=request.data['data']['postId'])
        except Post.DoesNotExist:
            return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.filter(creatorId=request.data['data']['creatorId']).filter(
            postId=request.data['data']['postId'])
        request.data['data']['postCreatorId'] = post.fromId
        if comment:
            return Response({'error': "User Already create a comment for this post."})
        else:
            serializer = CommentSerializer(data=request.data['data'])
            if serializer.is_valid():
                post.commentsCount += 1
                post.save()
                serializer.save()
                return Response(get_required_response(data=serializer.data))
            else:
                return Response(serializer.errors)


class PostCommentDetails(APIView):
    permission_classes = [IsIndividualUser, ]
    authentication_classes = [TokenAuthentication, ]

    def put(self, request, pk=None):
        if pk:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, data=request.data['data'])
            if serializer.is_valid():
                serializer.save()
                return Response(get_required_response(data=serializer.data))
            else:
                return Response(serializer.errors)

        else:
            try:
                post = Post.objects.get(pk=request.data['data']['postId'])
            except Post.DoesNotExist:
                return Response({'Error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            comment = Comment.objects.filter(creatorId=request.data['data']['creatorId']).filter(
                postId=request.data['data']['postId'])
            request.data['data']['postCreatorId'] = post.fromId
            serializer = CommentSerializer(comment[0], data=request.data['data'])
            if serializer.is_valid():
                serializer.save()
                return Response(get_required_response(data=serializer.data))
            else:
                return Response(serializer.errors)

    def delete(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        post = comment.postId
        comment.delete()
        post.commentsCount -= 1
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetToken(APIView):

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        token = Token.objects.get_or_create(user=user)
        print(token[0])
        return Response({"token": token[0].key})




