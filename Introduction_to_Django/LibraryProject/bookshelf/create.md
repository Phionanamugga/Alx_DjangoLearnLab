# Create Operation for Book Model

This file documents the Django shell command to create a `Book` instance.

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

