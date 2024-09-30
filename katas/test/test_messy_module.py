import inspect
import unittest
import os


class TestMessyModuleL2(unittest.TestCase):

    def test_xlibrary_package(self):
        self.assertTrue(os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'xlibrary')))
        self.assertTrue(os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'xlibrary', '__init__.py')))

    def test_imports(self):
        from katas.xlibrary import Book, Customer, Library, LibraryBranch, Librarian

        module = inspect.getmodule(Book)
        self.assertIsNotNone(module)
        self.assertFalse(module.__file__.endswith('xlibrary.py'))

        module = inspect.getmodule(Customer)
        self.assertIsNotNone(module)
        self.assertFalse(module.__file__.endswith('xlibrary.py'))

        module = inspect.getmodule(Library)
        self.assertIsNotNone(module)
        self.assertFalse(module.__file__.endswith('xlibrary.py'))

        module = inspect.getmodule(LibraryBranch)
        self.assertIsNotNone(module)
        self.assertFalse(module.__file__.endswith('xlibrary.py'))

        module = inspect.getmodule(Librarian)
        self.assertIsNotNone(module)
        self.assertFalse(module.__file__.endswith('xlibrary.py'))

    def test_operations(self):
        from katas.xlibrary import Book, Customer, Library, LibraryBranch, Librarian

        book1 = Book("Python Programming", "John Doe", "978-0-13-444432-1", 2022, 400)
        book2 = Book("Data Science Handbook", "Jane Smith", "978-0-12-644222-1", 2021, 500)
        customer1 = Customer("Alice", "alice@example.com", "123-456-7890")
        library = Library("City Central Library", "123 Main Street")
        branch1 = LibraryBranch("Main Branch", "123 Main Street")
        branch2 = LibraryBranch("West Branch", "456 Elm Street")
        library.add_branch(branch1)
        library.add_branch(branch2)
        librarian = Librarian("Bob", library)
        librarian.add_book_to_branch(book1, branch1)
        librarian.add_book_to_branch(book2, branch2)

        self.assertEqual(len(library.branches), 2)
        self.assertIn(branch1, library.branches)
        self.assertIn(branch2, library.branches)
        self.assertEqual(len(branch1.books), 1)
        self.assertEqual(len(branch2.books), 1)
        self.assertIn(book1, branch1.books)
        self.assertIn(book2, branch2.books)
        self.assertTrue(customer1.check_out_book(book1))
        self.assertTrue(customer1.check_out_book(book2))
        self.assertEqual(len(customer1.checked_out_books), 2)
        self.assertIn(book1, customer1.checked_out_books)
        self.assertIn(book2, customer1.checked_out_books)


if __name__ == '__main__':
    unittest.main()
