# Django Management Commands for Books

This directory contains custom Django management commands for managing book data in development.

## Available Commands

### 1. seed_books

Seeds the database with 15 sample books for development and testing purposes.

**Usage:**
```bash
python manage.py seed_books
```

**Features:**
- Creates 15 diverse sample books covering various categories
- Prevents duplicate records (checks ISBN before creating)
- Shows colored output for created/skipped books
- Displays summary with counts at the end
- Safe to run multiple times (won't create duplicates)

**Sample Output:**
```
Starting book seeding process...
✓ Created: "Python Crash Course" by Eric Matthes
✓ Created: "Clean Code" by Robert C. Martin
...
============================================================
✓ Seeding completed!
  - Books created: 15
  - Books skipped: 0
  - Total books in database: 15
============================================================
```

**Categories Included:**
- Programming
- Software Engineering
- Computer Science
- Artificial Intelligence

---

### 2. clear_books

Deletes all books from the database. Use with caution!

**Usage:**
```bash
python manage.py clear_books
```

**With confirmation skip:**
```bash
python manage.py clear_books --no-input
```

**Features:**
- Requires confirmation before deletion (unless --no-input flag is used)
- Lists all books being deleted
- Shows colored output for deleted books
- Displays summary with deletion count
- Safe guard: asks "Type 'yes' to confirm"

**Sample Output:**
```
⚠ WARNING: This will delete 15 book(s) from the database!
This action cannot be undone.

Are you sure you want to continue? Type "yes" to confirm: yes

Deleting books...
✗ Deleted: "Python Crash Course" by Eric Matthes
✗ Deleted: "Clean Code" by Robert C. Martin
...
============================================================
✓ All books cleared from database!
  - Total books deleted: 15
  - Remaining books: 0
============================================================
```

---

## Development Workflow

### Initial Setup
```bash
# Seed the database with sample data
python manage.py seed_books
```

### Reset Data
```bash
# Clear all books
python manage.py clear_books

# Re-seed with fresh data
python manage.py seed_books
```

### Quick Reset (No Confirmation)
```bash
python manage.py clear_books --no-input && python manage.py seed_books
```

---

## Notes

- **Development Only**: These commands are intended for development and testing environments only.
- **ISBN Uniqueness**: The seed command uses ISBN as a unique identifier to prevent duplicates.
- **Data Safety**: The clear_books command requires explicit confirmation to prevent accidental data loss.
- **Idempotent**: Running seed_books multiple times is safe - it won't create duplicates.

---

## Sample Books Included

The seed_books command includes 15 carefully selected technical books:

1. Python Crash Course - Eric Matthes
2. Clean Code - Robert C. Martin
3. The Pragmatic Programmer - Andrew Hunt
4. JavaScript: The Good Parts - Douglas Crockford
5. Design Patterns - Erich Gamma
6. Introduction to Algorithms - Thomas H. Cormen
7. Eloquent JavaScript - Marijn Haverbeke
8. You Don't Know JS - Kyle Simpson
9. Head First Design Patterns - Eric Freeman
10. The Mythical Man-Month - Frederick Brooks
11. Code Complete - Steve McConnell
12. Refactoring - Martin Fowler
13. Cracking the Coding Interview - Gayle Laakmann McDowell
14. Artificial Intelligence: A Modern Approach - Stuart Russell
15. Deep Learning - Ian Goodfellow

Each book includes:
- Realistic title and author
- Valid ISBN-13 number
- Category classification
- Detailed description
- Quantity and availability data
