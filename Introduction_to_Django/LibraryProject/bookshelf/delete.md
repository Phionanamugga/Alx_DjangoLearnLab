# Delete Operation for Book Model

This file documents the Django shell command to delete a `Book` instance.

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())