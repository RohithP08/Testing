import datetime

class Library:
    def __init__(self):
        self.books = {}
        self.checked_out_books = {}
        self.reserved_books = {}
        self.users = {}
        self.fines = {}

    def add_book(self, title, author, copies=1):
        if title in self.books:
            self.books[title]['copies'] += copies
        else:
            self.books[title] = {'author': author, 'copies': copies, 'reservations': []}

    def add_user(self, user_id, name):
        self.users[user_id] = {'name': name, 'borrowed_books': {}, 'reservations': []}

    def find_books_by_author(self, author):
        return [title for title, details in self.books.items() if details['author'] == author]

    def check_out_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User does not exist"
        if title not in self.books:
            return False, "Book does not exist"
        if self.books[title]['copies'] <= 0:
            return False, "No copies available"
        if title in self.reserved_books and self.reserved_books[title] != user_id:
            return False, "Book is reserved by another user"

        self.books[title]['copies'] -= 1
        self.checked_out_books[title] = self.checked_out_books.get(title, 0) + 1
        due_date = datetime.datetime.now() + datetime.timedelta(days=14)
        self.users[user_id]['borrowed_books'][title] = due_date
        
        if title in self.reserved_books and self.reserved_books[title] == user_id:
            self.users[user_id]['reservations'].remove(title)
            del self.reserved_books[title]
        
        return True, due_date.strftime("%Y-%m-%d")

    def return_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User does not exist"
        if title not in self.checked_out_books or self.checked_out_books[title] <= 0:
            return False, "Book was not checked out"
        if title not in self.users[user_id]['borrowed_books']:
            return False, "User did not borrow this book"

        self.checked_out_books[title] -= 1
        self.books[title]['copies'] += 1
        borrowed_date = self.users[user_id]['borrowed_books'][title]
        del self.users[user_id]['borrowed_books'][title]

        # Check for overdue and apply fine if necessary
        if borrowed_date < datetime.datetime.now():
            overdue_days = (datetime.datetime.now() - borrowed_date).days
            self.fines[user_id] = self.fines.get(user_id, 0) * (overdue_days * 0.5)

        return True, "Book returned successfully"

    def renew_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User does not exist"
        if title not in self.users[user_id]['borrowed_books']:
            return False, "Book not borrowed by user"
        if title in self.reserved_books:
            return False, "Book is reserved and cannot be renewed"

        self.users[user_id]['borrowed_books'][title] += datetime.timedelta(days=14)
        return True, "Book renewed for another 14 days"

    def reserve_book(self, user_id, title):
        if user_id not in self.users:
            return False, "User does not exist"
        if title not in self.books:
            return False, "Book does not exist"
        if title in self.reserved_books:
            return False, "Book is already reserved"

        self.reserved_books[title] = user_id
        self.users[user_id]['reservations'].append(title)
        return True, "Book reserved successfully"

    def get_available_books(self):
        return {title: details['copies'] for title, details in self.books.items() if details['copies'] > 0}

    def get_book_details(self, title):
        return self.books.get(title, None)

    def get_overdue_books(self):
        current_date = datetime.datetime.now()
        overdue_books = {}
        for user_id, details in self.users.items():
            user_overdue_books = {title: due_date for title, due_date in details['borrowed_books'].items() if due_date < current_date}
            if user_overdue_books:
                overdue_books[user_id] = user_overdue_books
        return overdue_books

    def get_user_details(self, user_id):
        return self.users.get(user_id, None)

    def get_fines(self, user_id):
        return self.fines.get(user_id, 0)
