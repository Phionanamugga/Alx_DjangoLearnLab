# Update Operation for Book Model

This file documents the Django shell command to update a `Book` instance.

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title, book.author, book.publication_year)