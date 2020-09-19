from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import RenewBookForm
from django.urls import reverse
import datetime


@login_required
def index(request):
    """Catalog index"""
    num_books = Book.objects.count()
    num_books_fantasy = Book.objects.filter(genre__name__exact='Fantasy').count()
    num_instances = BookInstance.objects.all().count()
    num_instances_HarryPotter = BookInstance.objects.filter(book__title__icontains='Harry Potter').count()
    num_authors = Author.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_books_fantasy': num_books_fantasy,
        'num_instances': num_instances,
        'num_instances_HarryPotter': num_instances_HarryPotter,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits,
    }
    return render(request, 'catalog/index.html', context=context)


class BooksList(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'


class AuthorsListView(ListView):
    model = Author
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'author'


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)


class AllLoanedBooksListView(PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'OOPS..Sorry. Not authorized!'

    model = BookInstance
    template_name = 'catalog/AllLoanedBooks_list.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-loaned-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class CreateAuthor(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'OOPS..Sorry. Not authorized!'
    model = Author
    fields = '__all__'


class UpdateAuthor(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'OOPS..Sorry. Not authorized!'
    model = Author
    fields = ('first_name', 'last_name')


class CreateBook(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'OOPS..Sorry. Not authorized!'
    model = Book
    fields = '__all__'


class UpdateBook(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    permission_denied_message = 'OOPS..Sorry. Not authorized!'
    model = Book
    fields = '__all__'
