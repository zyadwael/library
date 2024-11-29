from django.shortcuts import render, get_object_or_404,redirect
from .models import Book,Author,Borrow,Genre
from django.http import HttpResponseRedirect
from datetime import timedelta, date
from django.urls import reverse
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to the homepage or another page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_dashboard(request):
    borrowed_books = Borrow.objects.filter(user=request.user)
    today_date = now().strftime("%b. %d, %Y")  # Format today's date like the database
    return render(request, 'user_dashboard.html', {
        'borrowed_books': borrowed_books,
        'today_date': today_date
    })



def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})


def book_search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'book')

    if search_type == 'book':
        books = Book.objects.filter(title__icontains=query)
    elif search_type == 'author':
        books = Book.objects.filter(author__first_name__icontains=query) | Book.objects.filter(author__last_name__icontains=query)
    elif search_type == 'genre':
        books = Book.objects.filter(genre__name__icontains=query)
    else:
        books = Book.objects.none()  # Return an empty queryset if no valid search type is selected

    return render(request, 'book_search.html', {'books': books, 'query': query})


def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies > 0:
        book.available_copies -= 1
        book.save()
        Borrow.objects.create(
            book=book,
            user=request.user,
            due_date=date.today() + timedelta(days=14)
        )
    return HttpResponseRedirect(reverse('book_list'))


@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    
    # Get the book associated with the borrow record
    book = borrow.book
    
    # Increment the available copies of the book
    book.available_copies += 1
    book.save()
    
    # Delete the borrow record (book returned)
    borrow.delete()
    
    # Redirect to the user's dashboard after returning the book
    return redirect('user_dashboard')