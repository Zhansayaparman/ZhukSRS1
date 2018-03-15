from django.shortcuts import render

# Create your views here.
from .models import Tort, Konditer, Tort_id, Dami

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_torts=Tort.objects.all().count()
    num_id=Tort_id.objects.all().count()
    # Available torts (status = 'a')
    num_id_available=Tort.objects.filter(status__exact='a').count()
    num_konditers=Konditer.objects.count()  # The 'all()' is implied by default.
    
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+3
    
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_torts':num_torts,'num_id':num_id,'num_id_available':num_id_available,'num_konditers':num_konditers,
            'num_visits':num_visits}, # num_visits appended
    )
from django.views import generic

class TortListView(generic.ListView):
    model = Tort
    paginate_by = 3
class BookDetailView(generic.DetailView):
    model = Tort
from django.views import generic

class KonditerListView(generic.ListView):
    model = Konditer
class KonditerDetailView(generic.DetailView):
    model = Konditer
    model2=Tort
    paginate_by = 3
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = Tort_id
    template_name ='catalog/tort_id_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Tort_id.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewTortForm

@permission_required('catalog.can_mark_returned')
def renew_tort_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    tort_inst=get_object_or_404(Tort_id, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewTortFormForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            tort_inst_inst.due_back = form.cleaned_data['renewal_date']
            tort_inst_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewTortFormForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/tort_renew_librarian.html', {'form': form, 'tortinst':tort_inst})