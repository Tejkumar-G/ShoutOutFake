from django.urls import path
from .views import (
    ChallengesList,
    ChallengeDetail,
    CreatePost,
    EditPost,
    CreateProductReview,
    CreateProductCategory,
    TagsList,
    UsersList,
    DesignationsList,
    RolesList,
    PostLikeDetails,
    PostCommentsList,
    PostCommentDetails,
    GetToken,
    ResourcesList,
    ChallengeMapList,
    ChallengeMapDetail,
)

urlpatterns = [
    path('challenges/', ChallengesList.as_view(), name='challenges'),
    path('create-challenge/', ChallengesList.as_view(), name='challenges'),
    path('challenge/<int:pk>/', ChallengeDetail.as_view(), name='challenge-detail'),

    path('posts/', CreatePost.as_view(), name='posts'),
    path('create-post/', CreatePost.as_view(), name='create-post'),
    path('post/<int:pk>/', EditPost.as_view(), name='edit-post'),

    path('product-category/', CreateProductCategory.as_view(), name='product-category'),
    path('create-product-category/', CreateProductCategory.as_view(), name='create-product-category'),

    path('product-rewards/', CreateProductReview.as_view(), name='product-rewards'),
    path('create-product-reward/', CreateProductReview.as_view(), name='create-product-reward'),

    path('tags/', TagsList.as_view(), name='tags'),
    path('create-tag/', TagsList.as_view(), name='create-tag'),

    path('resources/', ResourcesList.as_view(), name='resources'),
    path('create-resource/', ResourcesList.as_view(), name='create-resource'),

    path('users/', UsersList.as_view(), name='user'),
    path('create-user/', UsersList.as_view(), name='create-user'),

    path('designation/', DesignationsList.as_view(), name='designation'),
    path('create-designation/', DesignationsList.as_view(), name='create-designation'),

    path('roles/', RolesList.as_view(), name='roles'),
    path('create-role/', RolesList.as_view(), name='create-role'),

    path('post/like', PostLikeDetails.as_view(), name='update-post'),
    path('post/<int:pk>/likes/', PostLikeDetails.as_view(), name='post-details'),

    path('post/comment/', PostCommentsList.as_view(), name='create-comment'),
    path('post/<int:pk>/comments/', PostCommentsList.as_view(), name='post-comments'),
    path('post/comment/<int:pk>/', PostCommentDetails.as_view(), name='edit-comment'),
    path('post/comment/<int:pk>/', PostCommentDetails.as_view(), name='delete-comment'),

    path('get_user_token/user/<int:pk>/', GetToken.as_view(), name='get-token'),

    path('get_challenges_details/', ChallengeMapList.as_view(), name='challenge-maps'),
    path('apply-challenge/', ChallengeMapList.as_view(), name='apply-challenge'),
    path('edit-challenge/<int:pk>', ChallengeMapDetail.as_view(), name='edit-challenge'),

]
