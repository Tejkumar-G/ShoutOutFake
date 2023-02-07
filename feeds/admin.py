from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Challenge,
    Comment,
    Post,
    ProductReward,
    Resource,
    User,
    Room,
    SpecialReward,
    Tag,
)


admin.site.register(Challenge)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(ProductReward)
admin.site.register(Resource)
admin.site.register(User, UserAdmin)
admin.site.register(Room)
admin.site.register(SpecialReward)
admin.site.register(Tag)
