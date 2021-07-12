# Design library database management system which hold records of books.
# A student should be able to allocate book (which is not assigned to anyone else) for specific period duration (such as 2 weeks).
# The librarian can add new books, delete existing books, view information for any book and update status for any book (assigned or not assigned).
# The student can request for book, which will be allocated if the book is available free in the library or else appropriate message will be displayed.

#Python Library
import re
from random import sample
from datetime import datetime, timedelta


class LibraryDatabaseManagementSystem:
    """
    Library Management System has 2 page views and exit from appication
    ***** MAIN MENU *****
    1. Admin page
    2. Student page
    3. Exit the application

    ***** ADMIN PRIVILAGES *****
    Admin page helps to maintain the books information
    Admin can add new books, delete old books, and assign or cancel the books to the students through 'view student requests'
    ***** ADMIN MENU *****
    1. Add new book
    2. Delete book
    3. View student requests
    4. Logout

    ***** STUDENT PRIVILAGES *****
    Student can register themself.
    Registered student can request a book for that have to login to his account
    ***** STUDENT PAGE *****
    1. New Student Register
    2. Signin your account
    3. Exit to home page

    """
    def __init__(self):
        """
        Constructor function helps to run entire application
        We have the option to choose from menu to do Admin or Student.
        """
        #Initializing empty dictionary for maintain books and students data
        self.books = {}
        self.students = {}
        #Sample data structure
        # self.books = {1: {'book_name': 'You can win', 'book_author': 'shiv', 'status': 'Not Assigned'}, 2: {'book_name': 'Think and Grow Rich', 'book_author': 'Neppolian Hill', 'status': 'Not Assigned'}, 3: {'book_name': 'Rich Dad Poor Dad', 'book_author': 'Robert', 'status': 'Not Assigned'}, 4: {'book_name': '5 Am Club', 'book_author': 'Robin Sharma', 'status': 'Not Assigned'}}
        # self.students = {'ananiastnj': {'student_name': 'Antony', 'student_password': 'ananiastnj', 'requested_book': [], 'assigned_book': []}, 'ananiastnj71': {'student_name': 'Ananias', 'student_password': 'ananiastnj71', 'requested_book': [], 'assigned_book': []}}

        # Choose 3 to end the loop. Other options continues the loop.
        while True:
            print_info("***** MAIN MENU *****",r=100, g=100, b=100)
            print_info("Do you want to login as Admin or Student")
            print_info("1. Admin page")
            print_info("2. Student page")
            print_info("3. Exit the application")
            # try block validates Value error
            try:
                #Enter your choice between 1 - 3
                choice = int(input("Choose the option to enter into the account: "))
                # if you entered choice is 1, calls the admin account
                if choice==1:
                    self.admin_account()
                # if you entered choice is 2, calls the student account
                elif choice==2:
                    self.student_account()
                # if you entered choice is 3, Exit from the applciation
                elif choice==3:
                    print_info("***** Thank You *****",r=100)
                    break
                # False block
                else:
                    print_error("Please choose the option from the menu(1-3)")
            except ValueError:
                print_error("Please enter number only")

    def admin_account(self):
        """
        This method helps admin to login and do the admin works
        :return: None
        """
        count = 0
        while count < 5:
            uname = input("Enter your username: ")
            pword = input("Enter your password: ")
            if uname == 'admin' and pword == 'admin':
                count = 5
                print("You logged in successfully")
                while True:
                    print_info("***** ADMIN MENU *****")
                    print_info("1. Add new book")
                    print_info("2. Delete book")
                    print_info("3. View student requests")
                    print_info("4. Logout")
                    try:
                        choice = int(input("Choose the option to enter into the account: "))
                        if choice==1:
                            self.add_new_book()
                        elif choice==2:
                            self.delete_book()
                        elif choice==3:
                            self.view_student_request()
                        elif choice==4:
                            print_info("***** Thank You Admin *****")
                            break
                        else:
                            print_error("Please choose the option from the menu(1-4)")
                    except ValueError:
                        print_error("Please enter number only")
            elif count < 5:
                count += 1
                print("You entered wrong username or password, try again. You have {} more attempts".format(5-count))
            else:
                print_error("You don't have options to try again, please contact application admin")
                break

    def add_new_book(self):
        """
        Method to add new books in the library.
        Through this method able to add only one book at a time.
        :return:
        """
        while True:
            print("Enter the Book details below")
            book_name = input("Enter the Book name: ")
            book_author = input("Enter the author: ")
            book_id = 1 if len(self.books)==0 else max(self.books.keys())+1
            self.books[book_id] = {'book_name' : book_name, 'book_author' : book_author, 'status' : 'Not Assigned'}
            cont = input("Do you like to add another book press Y, else press any key to exit: ")
            if cont.lower()=="y":
                continue
            break
        #Shows the table view of added books
        self.show_books(self.books)

    def show_books(self,books):
        """
        Method to show the registered books in the table format
        :param books: dictionary data to show the values
        :return: None
        """
        max_book_name_length = max([len(book['book_name']) for id,book in books.items()])
        max_book_author_length = max([len(book['book_author']) for id, book in books.items()])
        max_book_author_length = len("Book Author ") if len("Book Author ") > max_book_author_length else max_book_author_length
        print_info("{:<10} |{} |{} |{:<13} |{:<10} |{:<10} |{:<13} ".format('Book ID', 'Book Name'.ljust(max_book_name_length), 'Book Author'.ljust(max_book_author_length), 'Status', 'As.Date', 'Due Date', 'S.Username'))
        print_info("{} |{} |{} |{} |{} |{} |{}".format("-"*10,"-"*max_book_name_length,"-"*max_book_author_length,"-"*13,"-"*10,"-"*10, "-"*13))
        for id, book in books.items():
            print_info("{:<10} |{} |{} |{:<13} |{:<10} |{:<10} |{:<13}".format(id, book['book_name'].ljust(max_book_name_length), book['book_author'].ljust(max_book_author_length),book['status'], book.get('assigned_date', "NA"), book.get('due_date', "NA"), book.get('student_username', "NA")))

    def delete_book(self):
        """
        Method to delete the books.
        :return: None
        """
        #shows all the books in the library
        self.show_books(self.books)
        #book_id to delete the books
        book_id = int(input("Enter the book id to delete: "))
        try:
            self.books.pop(book_id)
        except KeyError:
            # throws the error message if book_id is not exist
            print_error("Book ID {} is not exist".format(book_id))
        self.show_books(self.books)

    def view_student_request(self):
        """
        Method to check books requested by student
        :return: None
        """
        requested_books = {}
        # loops to get only requested books
        for id, book in self.books.items():
            if book['status'].lower()=="requested":
                requested_books[id] = self.books[id]
        #if we have request books, it calls the method assign_books
        #if we have 0 request books,
        if len(requested_books) > 0:
            self.show_books(requested_books)
            self.assign_books()
        elif len(requested_books)==0:
            print_info("No books have been requested")

    def assign_books(self):
        """
        Method to assign or cancel the books to requested student
        Updates self.books and self.students data
        :return: None
        """
        print("Do you like to assign books to Students")
        # Using below dictionary comprehensions to get all the requested books
        requested_books = {id:student['requested_book'] for id, student in self.students.items() if len(student['requested_book'])>0}.copy()
        for id, requested_book in requested_books.items():
            while len(requested_book) > 0:
                try:
                    ind = 0
                    book = self.students[id]['requested_book'].pop(ind)
                    key = list(book.keys())[0]
                    print_info("'{}' requested by '{}'".format(book[key]['book_name'],book[key]['student_username']))
                    print_info("1. Assign")
                    print_info("2. Cancel")
                    choice = int(input("Enter your choice: "))
                    if choice==1:
                        book[key]['assigned_date'] = str(datetime.now()).split(".")[0]
                        book[key]['status'] = "Assigned"
                        book[key]['due_date'] = str(datetime.now()+timedelta(14)).split(".")[0]
                        self.books[key]['status'] = 'Assigned'
                        self.books[key]['assigned_date'] = str(datetime.now()).split(" ")[0]
                        self.books[key]['due_date'] = str(datetime.now()+timedelta(14)).split(" ")[0]
                        self.books[key]['student_username'] = id
                        self.students[id]['assigned_book'].append(book)
                    elif choice==2:
                        book[key]['status'] = 'Cancel'
                        book[key]['cancel_date'] = str(datetime.now()).split(".")[0]
                        self.books[key]['status'] = 'Not Assigned'
                        if 'canceled_book' not in self.students[id].keys():
                            self.students[id]['canceled_book'] = [book]
                        else:
                            self.students[id]['canceled_book'].append(book)
                    else:
                        print_error("Please choose 1 or 2")
                except ValueError:
                    print_error("Please Enter number only")
        print("All books are assigned/canceled successfully")

    def student_account(self):
        """
        Method to Student can register themself, signin, or exit to home page
        :return: None
        """
        while True:
            print_info("***** STUDENT PAGE *****")
            print_info("1. New Student Register")
            print_info("2. Signin your account")
            print_info("3. Exit to home page")
            try:
                choice = int(input("Enter your choice: "))
                if choice==1:
                    self.register_new_student()
                elif choice==2:
                    self.student_login()
                elif choice==3:
                    print_info("***** Exit from student page *****")
                    break
                else:
                    print_error("Please choose the number between 1-3")
            except ValueError:
                print_error("Please enter number only")

    def register_new_student(self):
        """
        Method to register new student
        :return: None
        """
        print_info("***** STUDENT DETAILS *****")
        student_name = input("Enter the your name: ")
        while True:
            student_username = input("Enter the your username: ")
            if student_username not in self.students.keys():
                #If it is new username, the loop end
                break
            print_error("username '{}' already exist".format(student_username))
            # If username is already exist, it suggest new 5 usernames for the student
            self.suggest_username(student_username)
        while True:
            student_password = input("Enter the your password: ")
            valid, msg = self.password_validation(student_password)
            if valid:
                # If it is valid password, the loop end
                break
            print_error(msg)
        # New student data is updated in self.students
        self.students[student_username] = {'student_name' : student_name,
                                           'student_password': student_password,
                                           'requested_book' : [],
                                           'assigned_book' : [],
                                           'canceled_book' : []
                                           }
        print_info("Student registered successfully")

    def suggest_username(self, username):
        """
        Method to suggest new usernames
        :param username: already existing username
        :return: None
        """
        suggest_usernames = [username+str(num) for num in range(1, 100) if username+str(num) not in self.students.keys()]
        print("We suggeste following usernames: ",end=" ")
        for ind, uname in enumerate(sample(suggest_usernames,5)):
            if ind!=4:
                print(uname,end=",")
            else:
                print(uname)

    def student_login(self):
        """
        Registered student can login to the account
        If we entered username or password wrong 5 times, this method goes to student home page
        :return: None
        """
        count = 0
        while count <= 5:
            if count==5:
                print("You are exceeding the attempts, Exit to Student Page")
                break
            print_info("***** STUDENT LOGIN *****")
            username = input("Enter your username: ")
            #Validating the username
            if username not in self.students.keys():
                print_error("Username is not exsist")
                count += 1
                continue
            password = input("Enter your password: ")
            #Validating the password
            if self.students[username]['student_password']!=password:
                print_error("Password is not matched")
                count += 1
            elif username in self.students.keys() and self.students[username]['student_password']==password:
                #Username and Password is right to do the further progress
                count = 6
                while True:
                    print_info("***** STUDENT MENU *****")
                    print_info("1. View all books")
                    print_info("2. Search Books")
                    print_info("3. Request Books")
                    print_info("4. View profile")
                    print_info("5. Logout")
                    choice = int(input("Enter your choice: "))
                    if choice==1:
                        self.show_books()
                    elif choice==2:
                        self.search_books()
                    elif choice==3:
                        self.request_books(username)
                    elif choice==4:
                        self.view_profile(username)
                    elif choice==5:
                        print_info("Logout to home page")
                        break
                    else:
                        print_error("Pleae choose your option between 1-5")

    def search_books(self):
        """
        Method to search the books by name or author with relative words
        :return: None
        """
        # search_key might be half or full name of book or author
        search_key = input("Enter the book name or author name: ")
        search_key_match = {}
        # Loops to get all the books matched by search key
        for id, book in self.books.items():
            if search_key.lower() in book['book_name'].lower() or search_key.lower() in book['book_author'].lower():
                search_key_match[id] = self.books[id]
        if len(search_key_match)==0:
            # It print, if we don't have any search books
            print_info("You don't have mathced books or authors")
        elif len(search_key_match)>0:
            print_info("Your search matched with {} books".format(len(search_key_match)))
            # If search key matched it prints in the table format
            self.show_books(search_key_match)

    def request_books(self,student_username):
        """
        The method to request books by the student. This method update the self.books and self.student data.
        :param student_username: Requested book update in student username
        :return: None
        """
        self.show_books(self.books)
        request_book_id = int(input("Enter the book id to request: "))
        # If requested book id is exist and it's not assigned or requested by anyone
        if request_book_id in self.books.keys() and self.books[request_book_id]['status'] == "Not Assigned":
            self.books[request_book_id]['status'] = "Requested"
            self.books[request_book_id]['student_username'] = student_username
            #Datetime converted to following string format '2021-07-09 08:41:19'
            self.books[request_book_id]['Requested_date'] = str(datetime.now()).split(".")[0]
            self.students[student_username]['requested_book'].append({request_book_id:self.books[request_book_id]})
            print_info("'{}' book has been requested successfully".format(self.books[request_book_id]['book_name']))
        elif request_book_id in self.books.keys() and self.books[request_book_id]['status'] != "Not Assigned":
            print_error("Sorry, your requested book is Assigned or Requested already")

    def view_profile(self, student_username):
        """
        Method to view student profile by himself
        :param student_username: student username to extract the student data
        :return: None
        """
        print("*"*50)
        print("Welcome {}".format(self.students[student_username]['student_name']))
        for key, value in self.students[student_username].items():
            if len(value) == 0:
                value = 'NA'
            print("{} : {}".format(" ".join(key.split("_")).title(),value))
        print("*" * 50)

    def password_validation(self, password):
        '''
        Method to validate the password with below primary conditions
        Primary conditions for password validation :
        1. Minimum 8 characters.
        2. The alphabets must be between [a-z]
        3. At least one alphabet should be of Upper Case [A-Z]
        4. At least 1 number or digit between [0-9].
        5. At least 1 character from [ _ or @ or $ ].
        :param
            password: should be a string to validate password
        :return: True for valid password or False for not valid password
        '''
        if len(password) < 8:
            return (False, "Minimum 8 characters required")
        elif not re.search("[a-z]", password):
            return (False, "Atleast one lower case required")
        elif not re.search("[A-Z]", password):
            return (False, "Atleast one upper case required")
        elif not re.search("[0-9]", password):
            return (False, "Atlease one digit required")
        elif not re.search("[_@$]", password):
            return (False, "Atlease any one of _, @, $ charcter required")
        else:
            return (True, "Valid password")

def print_error(text, r=255, g=0, b=0):
    """
    Method print the error message
    :param text: string to print the message
    :param r: 0-255 - red color code
    :param g: 0-255 - green color code
    :param b: 0-255 - blue color code
    :return: None
    """
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text))

def print_info(text, r=0, g=0, b=255):
    """
    Method to print the info message
    :param text: string to print the message
    :param r: 0-255 - red color code
    :param g: 0-255 - green color code
    :param b: 0-255 - blue color code
    :return: None
    """
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text))

if __name__=='__main__':
    ldms = LibraryDatabaseManagementSystem()

