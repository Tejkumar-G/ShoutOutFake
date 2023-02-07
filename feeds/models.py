from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Challenge(models.Model):
    createOn = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True)
    imageUrl = models.CharField(max_length=200, null=True)
    isInternal = models.BooleanField(default=False)
    name = models.CharField(max_length=200, )
    points = models.IntegerField(default=0)
    updateOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class Tag(models.Model):
    name = models.CharField(max_length=200)
    updateOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class Designation(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.name}'


class Resource(models.Model):
    clientName = models.CharField(max_length=200)
    createOn = models.DateTimeField(auto_now_add=True)
    projectName = models.CharField(max_length=200)
    resourceName = models.CharField(max_length=200)
    updateOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # username = None
    createOn = models.DateTimeField(auto_now_add=True)
    designation = models.ForeignKey(Designation, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=200, unique=True)
    giveablePoint = models.IntegerField(default=0)
    handlingResources = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.DO_NOTHING,
                                          related_name='handlingResources')
    imageUrl = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)
    redeemPoint = models.IntegerField(default=0)
    reporter = models.ForeignKey('self', max_length=200, null=True, blank=True, on_delete=models.DO_NOTHING)
    roles = models.ManyToManyField(Role, blank=True)
    uid = models.BigAutoField(primary_key=True)
    workingResources = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.DO_NOTHING,
                                         related_name='workingResources')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.uid}'


class Post(models.Model):
    comment_text = models.CharField(max_length=200, )
    commentsCount = models.IntegerField(default=0, null=True)
    createOn = models.DateTimeField(auto_now_add=True)
    imageUrl = models.CharField(max_length=200, null=True)
    likes = models.JSONField(default=list, blank=True, null=True)
    points = models.IntegerField(default=0, null=True)
    fromId = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    to = models.TextField(null=True, )
    updateOn = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return f'{self.id}'


class Comment(models.Model):
    post_comment = models.CharField(max_length=200)
    createdOn = models.DateTimeField(auto_now_add=True)
    creatorId = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    parentCreatorId = models.IntegerField(null=True, )
    parentId = models.ForeignKey(Post or Challenge, on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.id}'


class ChallengeMap(models.Model):
    challengeId = models.ForeignKey(Challenge, on_delete=models.CASCADE, primary_key=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, primary_key=False)
    note = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, default='Pending', )
    attachments = models.JSONField(default=list, blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    creatorId = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False, related_name='creatorId_set')


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.id}'


class ProductReward(models.Model):
    brandName = models.CharField(max_length=200, null=True)
    category = models.OneToOneField(ProductCategory, null=True, on_delete=models.CASCADE)
    createOn = models.DateTimeField(auto_now_add=True)
    imageUrl = models.CharField(max_length=200, null=True)
    point = models.IntegerField(default=0)
    rangeFrom = models.IntegerField(default=0, null=True)
    rangeTo = models.IntegerField(default=0, null=True)
    updateOn = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}'


class Room(models.Model):
    chatType = models.CharField(max_length=200)
    createOn = models.DateTimeField(auto_now_add=True)
    isOneToOne = models.BooleanField()
    link_id = models.CharField(max_length=200)
    roomId = models.CharField(max_length=200)
    uids = models.TextField(null=True)
    updateOn = models.DateTimeField(auto_now=True)
    users = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}'


class SpecialReward(models.Model):
    createOn = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=200)
    isActive = models.BooleanField()
    name = models.CharField(max_length=200)
    productUrl = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    rewardAdmin = models.CharField(max_length=200)
    updateOn = models.DateTimeField(auto_now=True)
    userNote = models.BooleanField()

    def __str__(self):
        return f'{self.id}'


# SpecialReward or Room or ProductReward or ProductCategory or
#                             ChallengeMap or Comment or Post or User or Resource or
#                             Role or Designation or Tag or Challenge, on_delete=models.DO_NOTHING, default={},




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
