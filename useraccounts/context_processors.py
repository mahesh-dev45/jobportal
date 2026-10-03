from applications.models import Notification


def notification_count(request):

    unread_count = 0

    if request.user.is_authenticated:

        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return {
        'unread_notification_count': unread_count
    }