from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status ='a')
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Query for word filtering (case-insensitive) >>> bellow <<<

    # Get search query from the GET request (default to an empty string)
    search_word = request.GET.get('search_word', '').strip()

    # Perform case-insensitive search for books and genres containing the word
    num_books_containing_word = 0
    num_genres_containing_word = 0

    if search_word:  # Only perform the search if a word is provided
        num_books_containing_word = Book.objects.filter(title__icontains=search_word).count()
        num_genres_containing_word = Genre.objects.filter(name__icontains=search_word).count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instance_available,
        'num_authors': num_authors,
        'num_books_containing_word': num_books_containing_word,
        'num_genres_containing_word': num_genres_containing_word,
        'search_word': search_word, 
        # Pass the search word to the template
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    