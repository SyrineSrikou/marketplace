from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notification


@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)
    extra_id = request.GET.get('extra_id', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()
        if notification.notification_type == Notification.STORE:
            return redirect('dashboard:user_stores')
        elif notification.notification_type == Notification.ORDER:
            return redirect('dashboard:user_orders')
        elif notification.notification_type == Notification.TICKET:
            return redirect('support:tickets')

    return render(request, 'notifications.html')