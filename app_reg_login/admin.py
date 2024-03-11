from django.contrib import admin

# Register your models here.
from .models import User, Item, Transition, Bids, Comment, Advertisement


admin.site.register(User)
admin.site.register(Item)
admin.site.register(Transition)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(Advertisement)
