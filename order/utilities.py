from notifications.utilities import create_notification
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from cart.cart import Cart
from .models import Order, OrderItem
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def checkout(request,user,address, order_note, amount, order_number):
    user = request.user
    order = Order.objects.create(user=user, address=address, order_note=order_note, paid_amount=amount, order_number=order_number)
    for item in Cart(request):
        OrderItem.objects.create(order=order,user=user, product=item['product'], store=item['product'].store, price=item['product'].price, quantity=item['quantity'])
    
        order.stores.add(item['product'].store)

        # Reduce the quantity of the sold products
        product=item['product']
        product.stock -= item['quantity']
        product.save()

        create_notification(request, item['product'].store.owner, 'message', extra_id=order.id)
    ''' 
        
        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('order:order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
 '''
    return order
 

 
def notify_store(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for store in order.stores.all():
        to_email = store.owner.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'store': store})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()