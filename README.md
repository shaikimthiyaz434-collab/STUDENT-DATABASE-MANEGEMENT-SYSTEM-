Student Database Management System

Project Overview

The Student Database Management System is a Python-based application developed using SQLite to manage student information, academic performance, and attendance records in an organized manner.

The application provides a centralized system to store, retrieve, update, and manage student records. It also supports subject-wise examination marks and daily attendance tracking, making student record management easier and more efficient.

Key Features

1. Student Information Management

- Add new student records.
- Store student ID, full name, father's name, age, gender, phone, email, address, and course.
- View all registered students.
- View complete individual student profiles.
- Update existing student information.
- Delete student records.

2. Academic Marks Management

- Record subject-wise marks.
- Store examination names and dates.
- Validate obtained marks against maximum marks.
- Prevent duplicate subject and examination entries for the same student.

3. Attendance Management

- Record daily attendance.
- Maintain Present, Absent, and Late statuses.
- View individual attendance history.
- Calculate attendance percentage automatically.

4. Database Management

- Uses SQLite for structured data storage.
- Automatically creates the database and required tables.
- Maintains relationships between students, marks, and attendance.
- Uses primary keys and foreign keys to maintain data integrity.

Technologies Used

- Python 3 – Application development.
- SQLite – Database management.
- SQL – Data storage and retrieval.
- sqlite3 – Python database connectivity.

Project Structure

Student-Database-Management-System/
│
├── main.py
├── README.md
└── .gitignore

Note: The "students.db" database file is automatically created when the application runs for the first time.

Database Design

The application uses three relational database tables:

Table| Purpose
students| Stores personal and course details
marks| Stores subject-wise examination marks
attendance| Stores daily attendance records

Installation and Execution

Prerequisites

- Python 3 installed on your system.
- No external Python packages required.

Steps to Run

1. Download or clone this repository.
2. Open the project folder.
3. Open a terminal in the project directory.
4. Execute the following command:

python main.py

On some systems, use:

python3 main.py

The SQLite database and required tables will be created automatically.

Application Menu

The application provides the following operations:

1. Add Student
2. View All Students
3. View Complete Student Profile
4. Update Student Details
5. Delete Student
6. Add Marks
7. Record Attendance
8. View Attendance Report
9. Exit

Learning Outcomes

Through this project, I gained practical experience in:

- Python programming and function-based development.
- SQL queries and relational database management.
- CRUD operations (Create, Read, Update, Delete).
- Database connectivity using Python SQLite.
- Primary keys, foreign keys, and data integrity.
- Handling real-world student records and attendance data.

Future Enhancements

- Develop a graphical user interface.
- Add student login and administrator authentication.
- Generate downloadable academic reports.
- Add visual analytics for marks and attendance.
- Implement search and filtering options.

Author

Shaik Inthiyaz 

BCA Graduate | Python & SQL Enthusiast
