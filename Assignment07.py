# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   <Your Name Here>,<Date>,<Activity>
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.


class Person:
    """
           A class representing person data.

           Properties:
           - first_name (str): The student's first name.
           - last_name (str): The student's last name.

           ChangeLog:
           - JSpencer, 6.4.2025: Created the class.
           - JSpencer, 6.5.2025: Edited class to make gett&setter pairs for first_name \
           and last_name private
    """
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

# TODO Create a getter and setter for the first_name property
    @property
    def first_name(self):
        return self.__first_name.title()
    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == '':
            self.__first_name = value
        else:
            raise ValueError("Student first name should not contain numbers.")

# TODO Create a getter and setter for the last_name property
    @property
    def last_name(self):
        return self.__last_name.title()
    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == '':
            self.__last_name = value
        else:
            raise ValueError("Student last name should not contain numbers.")

# TODO Override the __str__() method to return Person data
    def __str__(self):
        return f'{self.first_name},{self.last_name}'

class Student(Person):
    """
       A collection data about students
       Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        course_name(str): The name of the course.

       ChangeLog: (Who, When, What)
       JSpencer,6/4/2025,Created Class
       JSpencer,6/5/2025,Edited Class to make course_name getter & setter pair private
       JSpencer,6/6/2025, Edited if/else statement for course_name to try/else statement \
       to fix ValueError on program start, Removed erroneous space in inheritance statement \
       (first_name =first_name) to fix read error on program start
       JSpencer,6.8.2025, Edited setter for clearer code

    """
# TODO call to the Person constructor and pass it the first_name and last_name data
    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name
# TODO add the getter for course_name
    @property
    def course_name(self):
        return self.__course_name
# TODO add the setter for course_name
    @course_name.setter
    def course_name(self, value: str):
        if value != '':
            self.__course_name = value
        else:
            raise ValueError("Course name must be alphanumeric.")

# TODO Override the __str__() method to return the Student data
    def __str__(self):
        return f'{self.first_name},{self.last_name}, {self.course_name}'



# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows
        then returns the list filled with student data.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        JSpencer,6.8.2025, Edited function to convert dict data to student object data

        :param file_name: string data with name of file to read from

        :return: list
        """

        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert the list of dictionary rows into a list of Student objects
            # TODO replace this line of code to convert dictionary data to Student data
            for student in json_students:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)
                file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        JSpencer,6.8.2025 - Edited function to convert student obj into dict

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """

        try:
            # TODO Add code to convert Student objects into dictionaries (Done)
            json_students: list = []
            for student in student_data:
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name,
                       "CourseName": student.course_name}
                json_students.append(student_json)
            file = open(file_name, "w")
            json.dump(json_students, file, indent=2)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        JSpencer,6.8.2025 - Edited function to access student object data instead of dict data
        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:

            # TODO Add code to access Student object data instead of dictionary data
            print(f'Student {student.first_name} {student.last_name} '
                  f'is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        JSpencer,6.8.2025 - Edited function to use student objects instead of dict objects
        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            first_name = input("Enter the student's first name: ")
            if not first_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            last_name = input("Enter the student's last name: ")
            if not last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")

            # TODO Replace this code to use a Student objects instead of a dictionary objects
            student = Student(first_name=first_name,
                              last_name=last_name,
                              course_name=course_name)
            student_data.append(student)
            print()
            print(f"You have registered {first_name} {last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
