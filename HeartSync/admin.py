from django.contrib import admin

# Register your models here.
from django.contrib import admin
from HeartSync.models import City, Interest, UserProfile, Like, Match, Message, Block

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_id', 'city_name', 'state', 'country']
    search_fields = ['city_name', 'state', 'country']
    list_filter = ['state', 'country']
    ordering = ['city_name']

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['interest_id', 'interest_name']
    search_fields = ['interest_name']
    ordering = ['interest_name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'profile_id',
        'profile_picture',
        'firstname',
        'lastname',
        'gender',
        'age',
        'profession',
        'city',
        'is_active',
        'joined_at',
    ]
    search_fields = ['name', 'email', 'profession', 'city__city_name']
    list_filter = ['gender', 'age', 'city', 'is_active', 'joined_at']
    ordering = ['-joined_at']
    filter_horizontal = ['interests']
    list_editable = ['is_active']
    readonly_fields = ['joined_at']
    list_select_related = ['city']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'liked_at']
    search_fields = ['sender__name', 'receiver__name']
    list_filter = ['liked_at']
    ordering = ['-liked_at']
    readonly_fields = ['liked_at']
    list_select_related = ['sender', 'receiver']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_user',
        'second_user',
        'matched_at',
        'is_active',
    ]
    search_fields = ['first_user__name', 'second_user__name']
    list_filter = ['is_active', 'matched_at']
    ordering = ['-matched_at']
    list_editable = ['is_active']
    readonly_fields = ['matched_at']
    list_select_related = ['first_user', 'second_user']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'match',
        'sender',
        'short_message',
        'sent_at',
        'is_read',
    ]
    search_fields = ['sender__name', 'message']
    list_filter = ['is_read', 'sent_at']
    ordering = ['-sent_at']
    list_editable = ['is_read']
    readonly_fields = ['sent_at']
    list_select_related = ['match', 'sender']

    @admin.display(description='Message')
    def short_message(self, obj):
        if len(obj.message) > 40:
            return f'{obj.message[:40]}...'
        return obj.message

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['id', 'blocker', 'blocked_user', 'blocked_at']
    search_fields = ['blocker__name', 'blocked_user__name']
    list_filter = ['blocked_at']
    ordering = ['-blocked_at']
    readonly_fields = ['blocked_at']
    list_select_related = ['blocker', 'blocked_user']