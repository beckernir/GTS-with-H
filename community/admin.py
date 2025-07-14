from django.contrib import admin
from .models import CommunityForum, ForumTopic, ForumPost, CommunityMessage, Feedback, Announcement, CommunityEvent

# Register your models here.
admin.site.register(CommunityForum)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
admin.site.register(CommunityMessage)
admin.site.register(Feedback)
admin.site.register(Announcement)
admin.site.register(CommunityEvent)
