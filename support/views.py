from notifications.utilities import create_notification
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import ConversationMessage, Ticket
from .forms import TicketForm
#from notifications.signals import notify
# Create your views here.


#tickets
@login_required(login_url='accounts:login')
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            form.save()
            return redirect('support:tickets')
    else:
        form = TicketForm()
    
    return render(request, 'create-ticket.html', {'form': form})



@login_required(login_url='accounts:login')
def tickets(request):
    user = request.user
    tickets = user.ticket_set.all().order_by("-id")
    
    paginator = Paginator(tickets,2)
    page = request.GET.get('page')
    paged_tickets = paginator.get_page(page)
    return render(request, 'tickets.html', {'tickets': paged_tickets})


@login_required(login_url='accounts:login')
def single_ticket(request):
    return render(request, 'single_ticket.html')




@login_required(login_url='accounts:login')
def single_ticket(request, ticket_id):
    if request.user.is_staff == True:
        ticket = get_object_or_404(Ticket, pk=ticket_id, created_by=request.user)
    else:
        ticket = get_object_or_404(Ticket, pk=ticket_id,)
    
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            conversationmessage = ConversationMessage.objects.create(ticket=ticket, content=content, created_by=request.user)
            create_notification(request, ticket.created_by, 'message + f" <a href="tickets/single_ticket/{ticket.id}"> Go </a>" ', extra_id=ticket.id)
            
            return redirect('support:single_ticket', ticket_id=ticket.id)
    
    return render(request, 'single_ticket.html', {'ticket': ticket})
