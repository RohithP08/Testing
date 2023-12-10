import unittest
from library import Library
import datetime

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.add_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", 3)
        self.library.add_user("u1", "John Doe")

    def test_add_book(self):
        self.library.add_book("1984", "George Orwell")
        book_details = self.library.get_book_details("1984")
        self.assertIsNotNone(book_details)
        self.assertEqual(book_details['author'], "George Orwell")
        self.assertEqual(book_details['copies'], 1)

    def test_add_user(self):
        self.library.add_user("u2", "Jane Smith")
        user_details = self.library.get_user_details("u2")
        self.assertIsNotNone(user_details)
        self.assertEqual(user_details['name'], "Jane Smith")

    def test_check_out_book(self):
        success, _ = self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.assertTrue(success)
        self.assertEqual(self.library.get_available_books()["The Hitchhiker's Guide to the Galaxy"], 2)

    def test_check_out_book_unavailable(self):
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        success, _ = self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.assertFalse(success)

    def test_return_book(self):
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        success, _ = self.library.return_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.assertTrue(success)

    def test_return_book_not_borrowed(self):
        success, _ = self.library.return_book("u1", "1984")
        self.assertFalse(success)

    def test_renew_book(self):
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        success, message = self.library.renew_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.assertTrue(success)
        self.assertEqual(message, "Book renewed for another 14 days")

    def test_renew_unborrowed_book(self):
        success, message = self.library.renew_book("u1", "1984")
        self.assertFalse(success)
        self.assertEqual(message, "Book not borrowed by user")

    def test_reserve_book(self):
        success, message = self.library.reserve_book("u1", "The Hitchhiker's Guide to the Galaxy")
        self.assertTrue(success)
        self.assertEqual(message, "Book reserved successfully")

    def test_reserve_already_reserved_book(self):
        self.library.add_user("u2", "Jane Doe")  # Ensure the second user is added.
        self.library.reserve_book("u1", "The Hitchhiker's Guide to the Galaxy")
        success, message = self.library.reserve_book("u2", "The Hitchhiker's Guide to the Galaxy")
        self.assertFalse(success)
        self.assertEqual(message, "Book is already reserved")


    def test_get_overdue_books(self):
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        # Manually setting the due date to the past to simulate an overdue book
        past_due_date = datetime.datetime.now() - datetime.timedelta(days=30)
        self.library.users["u1"]['borrowed_books']["The Hitchhiker's Guide to the Galaxy"] = past_due_date
        overdue_books = self.library.get_overdue_books()
        self.assertIn("u1", overdue_books)
        self.assertIn("The Hitchhiker's Guide to the Galaxy", overdue_books["u1"])

    def test_fines_for_overdue_books(self):
        self.library.check_out_book("u1", "The Hitchhiker's Guide to the Galaxy")
        # Simulate an overdue book
        past_due_date = datetime.datetime.now() - datetime.timedelta(days=30)
        self.library.users["u1"]['borrowed_books']["The Hitchhiker's Guide to the Galaxy"] = past_due_date
        self.library.return_book("u1", "The Hitchhiker's Guide to the Galaxy")
        fine = self.library.get_fines("u1")
        self.assertGreater(fine, 0)

if __name__ == '__main__':
    unittest.main()
