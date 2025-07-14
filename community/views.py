from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CommunityForum, ForumTopic, ForumPost, Announcement, CommunityEvent, CommunityMessage
from .forms import CommunityForumForm, ForumTopicForm, ForumPostForm, AnnouncementForm, CommunityEventForm, CommunityMessageForm
from django.db.models import Count
from core.models import User
from datetime import datetime
from django.views.decorators.http import require_GET

# Create your views here.

def community_overview_view(request):
    # Community stats
    total_members = User.objects.filter(is_active=True).count()
    active_discussions = ForumTopic.objects.filter(status='active').count()
    total_posts = ForumPost.objects.filter(status='active').count()
    now = datetime.now()
    events_this_month = CommunityEvent.objects.filter(start_date__year=now.year, start_date__month=now.month).count()

    # Featured discussions: 3 most recent active topics
    featured_discussions = ForumTopic.objects.filter(status='active').order_by('-last_activity')[:3]

    # Upcoming events: 3 soonest upcoming events
    upcoming_events = CommunityEvent.objects.filter(start_date__gte=now).order_by('start_date')[:3]

    # Discussion categories: forum_type and count
    categories = CommunityForum.objects.values('forum_type').annotate(count=Count('id')).order_by('forum_type')

    # Top contributors: users with most posts
    top_contributors = User.objects.annotate(post_count=Count('forum_posts')).filter(post_count__gt=0).order_by('-post_count')[:3]

    context = {
        'total_members': total_members,
        'active_discussions': active_discussions,
        'total_posts': total_posts,
        'events_this_month': events_this_month,
        'featured_discussions': featured_discussions,
        'upcoming_events': upcoming_events,
        'categories': categories,
        'top_contributors': top_contributors,
    }
    return render(request, "community/overview.html", context)

@login_required
def forum_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        forums = CommunityForum.objects.all().order_by('forum_type', 'forum_name')
    elif hasattr(user, 'is_school_admin') and user.is_school_admin():
        forums = CommunityForum.objects.filter(school__user_assignments__user=user).order_by('forum_type', 'forum_name')
    else:
        forums = CommunityForum.objects.filter(is_active=True, access_level__in=['public', 'registered_users']).order_by('forum_type', 'forum_name')
    return render(request, "community/forum_list.html", {'forums': forums})

@login_required
@user_passes_test(lambda u: (hasattr(u, 'is_school_admin') and u.is_school_admin()) or (hasattr(u, 'is_reb_officer') and u.is_reb_officer()) or (hasattr(u, 'is_system_admin') and u.is_system_admin()))
def forum_create_view(request):
    if request.method == 'POST':
        form = CommunityForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            form.save_m2m()
            return redirect('community:forum_list')
    else:
        form = CommunityForumForm()
    return render(request, "community/forum_create.html", {'form': form})

@login_required
def forum_edit_view(request, forum_id):
    forum = get_object_or_404(CommunityForum, forum_id=forum_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and forum.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CommunityForumForm(request.POST, instance=forum)
        if form.is_valid():
            form.save()
            return redirect('community:forum_detail', forum_id=forum.forum_id)
    else:
        form = CommunityForumForm(instance=forum)
    return render(request, "community/forum_edit.html", {'form': form, 'forum': forum})

@login_required
def forum_detail_view(request, forum_id):
    forum = get_object_or_404(CommunityForum, forum_id=forum_id)
    return render(request, "community/forum_detail.html", {'forum': forum})

@login_required
def topic_list_view(request, forum_id):
    forum = get_object_or_404(CommunityForum, forum_id=forum_id)
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()) or (hasattr(user, 'is_school_admin') and user.is_school_admin() and forum.school in [a.school for a in user.school_assignments.filter(is_active=True)]):
        topics = forum.topics.all().order_by('-is_sticky', '-last_activity')
    else:
        topics = forum.topics.filter(status='active').order_by('-is_sticky', '-last_activity')
    return render(request, "community/topic_list.html", {'forum': forum, 'topics': topics})

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_school_admin') and u.is_school_admin())
def topic_create_view(request, forum_id):
    forum = get_object_or_404(CommunityForum, forum_id=forum_id)
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.created_by = request.user
            topic.save()
            return redirect('community:topic_list', forum_id=forum.forum_id)
    else:
        form = ForumTopicForm(initial={'forum': forum})
    return render(request, "community/topic_create.html", {'form': form, 'forum': forum})

@login_required
def topic_edit_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, topic_id=topic_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and topic.forum.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ForumTopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('community:topic_detail', topic_id=topic.topic_id)
    else:
        form = ForumTopicForm(instance=topic)
    return render(request, "community/topic_edit.html", {'form': form, 'topic': topic})

@login_required
def topic_delete_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, topic_id=topic_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or (user.is_school_admin() and topic.forum.school in [a.school for a in user.school_assignments.filter(is_active=True)])):
        return HttpResponseForbidden()
    forum_id = topic.forum.forum_id
    if request.method == 'POST':
        topic.delete()
        return redirect('community:topic_list', forum_id=forum_id)
    return render(request, "community/topic_delete.html", {'topic': topic})

@login_required
def topic_detail_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, topic_id=topic_id)
    return render(request, "community/topic_detail.html", {'topic': topic})

@login_required
def post_list_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, topic_id=topic_id)
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()) or (hasattr(user, 'is_school_admin') and user.is_school_admin() and topic.forum.school in [a.school for a in user.school_assignments.filter(is_active=True)]):
        posts = topic.posts.all().order_by('created_at')
    else:
        posts = topic.posts.filter(status='active').order_by('created_at')
    return render(request, "community/post_list.html", {'topic': topic, 'posts': posts})

@login_required
def post_create_view(request, topic_id):
    topic = get_object_or_404(ForumTopic, topic_id=topic_id)
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('community:post_list', topic_id=topic.topic_id)
    else:
        form = ForumPostForm(initial={'topic': topic})
    return render(request, "community/post_create.html", {'form': form, 'topic': topic})

@login_required
def post_edit_view(request, post_id):
    post = get_object_or_404(ForumPost, post_id=post_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or post.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community:post_detail', post_id=post.post_id)
    else:
        form = ForumPostForm(instance=post)
    return render(request, "community/post_edit.html", {'form': form, 'post': post})

@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(ForumPost, post_id=post_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or post.created_by == user):
        return HttpResponseForbidden()
    topic_id = post.topic.topic_id
    if request.method == 'POST':
        post.delete()
        return redirect('community:post_list', topic_id=topic_id)
    return render(request, "community/post_delete.html", {'post': post})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(ForumPost, post_id=post_id)
    return render(request, "community/post_detail.html", {'post': post})

def post_reply_view(request, post_id):
    return render(request, "community/post_reply.html")

@login_required
def message_list_view(request):
    received = CommunityMessage.objects.filter(recipients=request.user).order_by('-created_at')
    sent = CommunityMessage.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, "community/message_list.html", {'received': received, 'sent': sent})

@login_required
def message_create_view(request):
    if request.method == 'POST':
        form = CommunityMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            form.cleaned_data['recipients']  # List of User objects
            msg.recipients.set(form.cleaned_data['recipients'])
            msg.save()
            return redirect('community:message_list')
    else:
        form = CommunityMessageForm()
    return render(request, "community/message_create.html", {'form': form})

@login_required
def message_detail_view(request, message_id):
    msg = get_object_or_404(CommunityMessage, message_id=message_id)
    if request.user != msg.sender and request.user not in msg.recipients.all():
        return HttpResponseForbidden()
    replies = CommunityMessage.objects.filter(replied_to=msg).order_by('created_at')
    return render(request, "community/message_detail.html", {'message': msg, 'replies': replies})

@login_required
def message_reply_view(request, message_id):
    parent = get_object_or_404(CommunityMessage, message_id=message_id)
    if request.user != parent.sender and request.user not in parent.recipients.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CommunityMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.replied_to = parent
            msg.save()
            msg.recipients.set(form.cleaned_data['recipients'])
            msg.save()
            return redirect('community:message_detail', message_id=parent.message_id)
    else:
        form = CommunityMessageForm()
    return render(request, "community/message_reply.html", {'form': form, 'parent': parent})

def message_delete_view(request, message_id):
    return render(request, "community/message_delete.html")

def feedback_list_view(request):
    return render(request, "community/feedback_list.html")

def feedback_create_view(request):
    return render(request, "community/feedback_create.html")

def feedback_detail_view(request, feedback_id):
    return render(request, "community/feedback_detail.html")

def feedback_edit_view(request, feedback_id):
    return render(request, "community/feedback_edit.html")

def feedback_resolve_view(request, feedback_id):
    return render(request, "community/feedback_resolve.html")

@login_required
def announcement_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        announcements = Announcement.objects.all().order_by('-priority', '-publish_date')
    else:
        announcements = Announcement.objects.filter(is_active=True).order_by('-priority', '-publish_date')
    return render(request, "community/announcement_list.html", {'announcements': announcements})

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_reb_officer') and u.is_reb_officer() or u.is_system_admin())
def announcement_create_view(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            form.save_m2m()
            return redirect('community:announcement_list')
    else:
        form = AnnouncementForm()
    return render(request, "community/announcement_create.html", {'form': form})

@login_required
def announcement_edit_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or announcement.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('community:announcement_detail', announcement_id=announcement.announcement_id)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "community/announcement_edit.html", {'form': form, 'announcement': announcement})

@login_required
def announcement_delete_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or announcement.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        announcement.delete()
        return redirect('community:announcement_list')
    return render(request, "community/announcement_delete.html", {'announcement': announcement})

@login_required
def announcement_detail_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, announcement_id=announcement_id)
    return render(request, "community/announcement_detail.html", {'announcement': announcement})

@login_required
def event_list_view(request):
    user = request.user
    if hasattr(user, 'is_reb_officer') and (user.is_reb_officer() or user.is_system_admin()):
        events = CommunityEvent.objects.all().order_by('-start_date')
    else:
        events = CommunityEvent.objects.filter(status__in=['published', 'registration_open', 'in_progress', 'completed']).order_by('-start_date')
    return render(request, "community/event_list.html", {'events': events})

@login_required
@user_passes_test(lambda u: hasattr(u, 'is_school_admin') and u.is_school_admin() or u.is_reb_officer() or u.is_system_admin())
def event_create_view(request):
    if request.method == 'POST':
        form = CommunityEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()
            return redirect('community:event_list')
    else:
        form = CommunityEventForm()
    return render(request, "community/event_create.html", {'form': form})

@login_required
def event_edit_view(request, event_id):
    event = get_object_or_404(CommunityEvent, event_id=event_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or event.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CommunityEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('community:event_detail', event_id=event.event_id)
    else:
        form = CommunityEventForm(instance=event)
    return render(request, "community/event_edit.html", {'form': form, 'event': event})

@login_required
def event_delete_view(request, event_id):
    event = get_object_or_404(CommunityEvent, event_id=event_id)
    user = request.user
    if not (user.is_reb_officer() or user.is_system_admin() or event.created_by == user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        event.delete()
        return redirect('community:event_list')
    return render(request, "community/event_delete.html", {'event': event})

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(CommunityEvent, event_id=event_id)
    return render(request, "community/event_detail.html", {'event': event})

def event_register_view(request, event_id):
    return render(request, "community/event_register.html")

def event_cancel_view(request, event_id):
    return render(request, "community/event_cancel.html")

@require_GET
@login_required
def user_suggestions(request):
    query = request.GET.get('q', '').strip()
    users = User.objects.filter(username__istartswith=query)[:10]
    return JsonResponse({'results': [u.username for u in users]})
