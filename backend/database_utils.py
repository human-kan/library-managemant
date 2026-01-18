import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "library_db")
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        conn = self.connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                if query.lstrip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = cursor.rowcount
                return result
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None

# CRUD Operations
def get_all_books():
    db = Database()
    return db.execute_query("SELECT * FROM books")

def add_book(title, author, isbn, quantity=1):
    db = Database()
    query = "INSERT INTO books (title, author, isbn, total_quantity, available_quantity) VALUES (%s, %s, %s, %s, %s)"
    return db.execute_query(query, (title, author, isbn, quantity, quantity))

def update_book(book_id, title, author, isbn, total_qty):
    db = Database()
    # Adjust available_qty based on change in total_qty
    book = db.execute_query("SELECT total_quantity, available_quantity FROM books WHERE id=%s", (book_id,))
    if book:
        diff = total_qty - book[0]['total_quantity']
        new_avail = book[0]['available_quantity'] + diff
        query = "UPDATE books SET title=%s, author=%s, isbn=%s, total_quantity=%s, available_quantity=%s WHERE id=%s"
        return db.execute_query(query, (title, author, isbn, total_qty, new_avail, book_id))
    return None

def delete_book(book_id):
    db = Database()
    query = "DELETE FROM books WHERE id=%s"
    return db.execute_query(query, (book_id,))

def borrow_book(book_id, borrower_name, borrower_contact, due_date):
    db = Database()
    # Check if book is available
    book = db.execute_query("SELECT available_quantity FROM books WHERE id=%s", (book_id,))
    if book and book[0]['available_quantity'] > 0:
        # Create borrowing record
        query_borrow = "INSERT INTO borrowings (book_id, borrower_name, borrower_contact, due_date) VALUES (%s, %s, %s, %s)"
        db.execute_query(query_borrow, (book_id, borrower_name, borrower_contact, due_date))
        # Update available quantity
        query_update = "UPDATE books SET available_quantity = available_quantity - 1 WHERE id=%s"
        return db.execute_query(query_update, (book_id,))
    return None

def return_book(book_id, borrowing_id):
    db = Database()
    # Update borrowing record with return date
    query_return = "UPDATE borrowings SET return_date=CURRENT_TIMESTAMP WHERE id=%s"
    db.execute_query(query_return, (borrowing_id,))
    # Update available quantity
    query_update = "UPDATE books SET available_quantity = available_quantity + 1 WHERE id=%s"
    return db.execute_query(query_update, (book_id,))

def get_borrowing_history(only_active=False):
    db = Database()
    query = """
        SELECT br.id as borrowing_id, b.id as book_id, b.title, br.borrower_name, br.borrower_contact, 
               br.borrow_date, br.due_date, br.return_date,
               DATEDIFF(IFNULL(br.return_date, CURRENT_TIMESTAMP), br.borrow_date) as days_held
        FROM borrowings br
        JOIN books b ON br.book_id = b.id
    """
    if only_active:
        query += " WHERE br.return_date IS NULL"
    query += " ORDER BY br.borrow_date DESC"
    return db.execute_query(query)

def get_overdue_books():
    db = Database()
    query = """
        SELECT br.id, b.title, br.borrower_name, br.borrower_contact, br.due_date
        FROM borrowings br
        JOIN books b ON br.book_id = b.id
        WHERE br.return_date IS NULL AND br.due_date < CURRENT_DATE
    """
    return db.execute_query(query)
