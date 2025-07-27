# Retrieve Operation for Book Model

This file documents the Django shell command to retrieve a `Book` instance.

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)