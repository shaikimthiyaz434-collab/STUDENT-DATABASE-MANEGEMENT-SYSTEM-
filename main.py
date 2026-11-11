"""Student Database Management System | Python + SQLite
Run: python main.py
The students.db database is created automatically.
"""
import sqlite3
from pathlib import Path
from datetime import date

DB = Path(__file__).with_name("students.db")

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def setup():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY, name TEXT NOT NULL, father_name TEXT NOT NULL,
            age INTEGER, gender TEXT, phone TEXT, email TEXT, address TEXT,
            course TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS marks(
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            subject TEXT NOT NULL, exam TEXT NOT NULL, obtained REAL NOT NULL,
            maximum REAL NOT NULL, exam_date TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            UNIQUE(student_id, subject, exam))""")
        c.execute("""CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT NOT NULL,
            attendance_date TEXT NOT NULL, status TEXT NOT NULL
            CHECK(status IN ('Present','Absent','Late')),
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            UNIQUE(student_id, attendance_date))""")

def ask(label):
    while True:
        v = input(label).strip()
        if v: return v
        print("This field is required.")

def valid_date(label):
    while True:
        v = input(label).strip()
        try: return date.fromisoformat(v).isoformat()
        except ValueError: print("Use YYYY-MM-DD format.")

def exists(sid):
    with db() as c:
        return c.execute("SELECT 1 FROM students WHERE student_id=?", (sid,)).fetchone() is not None

def add_student():
    print("\\n--- Add Student ---")
    sid = ask("Student ID: ")
    if exists(sid):
        print("That student ID already exists."); return
    name = ask("Student full name: ")
    father = ask("Father's name: ")
    age = input("Age (optional): ").strip()
    if age:
        try:
            age = int(age)
            if age < 1: raise ValueError
        except ValueError:
            print("Age must be a positive whole number."); return
    else: age = None
    gender = input("Gender (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    email = input("Email (optional): ").strip()
    address = input("Address (optional): ").strip()
    course = ask("Course: ")
    with db() as c:
        c.execute("""INSERT INTO students VALUES(?,?,?,?,?,?,?,?,?)""",
                  (sid,name,father,age,gender,phone,email,address,course))
    print("Student added successfully.")

def list_students():
    with db() as c:
        rows = c.execute("SELECT * FROM students ORDER BY student_id").fetchall()
    if not rows:
        print("No students found."); return
    print("\\n{:<14} {:<22} {:<22} {:<16} {}".format("STUDENT ID","NAME","FATHER","COURSE","PHONE"))
    print("-"*90)
    for r in rows:
        print("{:<14} {:<22} {:<22} {:<16} {}".format(
            r["student_id"][:13],r["name"][:21],r["father_name"][:21],
            r["course"][:15],r["phone"] or "-"))
    print("Total students:",len(rows))

def view_student():
    sid = ask("Student ID: ")
    with db() as c:
        s = c.execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone()
        if not s:
            print("Student not found."); return
        print("\\n--- PERSONAL DETAILS ---")
        for k,label in [("student_id","Student ID"),("name","Name"),("father_name","Father"),
                        ("age","Age"),("gender","Gender"),("phone","Phone"),("email","Email"),
                        ("address","Address"),("course","Course")]:
            print(f"{label}: {s[k] if s[k] not in (None,'') else '-'}")
        marks = c.execute("SELECT * FROM marks WHERE student_id=? ORDER BY exam_date",(sid,)).fetchall()
        att = c.execute("""SELECT COUNT(*) total,
            SUM(status='Present') present, SUM(status='Absent') absent,
            SUM(status='Late') late FROM attendance WHERE student_id=?""",(sid,)).fetchone()
    print("\\n--- MARKS ---")
    if marks:
        for m in marks:
            print(f"{m['subject']} | {m['exam']} | {m['obtained']:g}/{m['maximum']:g} | {m['exam_date'] or '-'}")
    else: print("No marks entered.")
    total = att["total"] or 0
    present, absent, late = att["present"] or 0, att["absent"] or 0, att["late"] or 0
    print("\\n--- ATTENDANCE ---")
    print(f"Recorded days: {total} | Present: {present} | Absent: {absent} | Late: {late}")
    print(f"Attendance: {(present+late)/total*100:.2f}%" if total else "Attendance: No records")

def update_student():
    sid = ask("Student ID to update: ")
    with db() as c:
        s = c.execute("SELECT * FROM students WHERE student_id=?", (sid,)).fetchone()
        if not s:
            print("Student not found."); return
        fields = [("name","Name"),("father_name","Father's name"),("gender","Gender"),
                  ("phone","Phone"),("email","Email"),("address","Address"),("course","Course")]
        changes = {}
        print("Press Enter to keep the current value.")
        for key,label in fields:
            value = input(f"{label} [{s[key] or ''}]: ").strip()
            if value: changes[key] = value
        age = input(f"Age [{s['age'] or ''}]: ").strip()
        if age:
            try:
                if int(age) < 1: raise ValueError
                changes["age"] = int(age)
            except ValueError:
                print("Invalid age; age was not changed.")
        if not changes:
            print("No changes made."); return
        sql = ", ".join(f"{k}=?" for k in changes)
        c.execute(f"UPDATE students SET {sql} WHERE student_id=?",
                  (*changes.values(),sid))
    print("Student details updated.")

def delete_student():
    sid = ask("Student ID to delete: ")
    if not exists(sid):
        print("Student not found."); return
    if input("Delete student and their marks/attendance? (y/n): ").lower() == "y":
        with db() as c:
            c.execute("DELETE FROM students WHERE student_id=?", (sid,))
        print("Student deleted.")
    else: print("Cancelled.")

def add_marks():
    sid = ask("Student ID: ")
    if not exists(sid):
        print("Student not found. Add student first."); return
    subject, exam = ask("Subject: "), ask("Exam name: ")
    try:
        obtained = float(input("Marks obtained: "))
        maximum = float(input("Maximum marks: "))
        if maximum <= 0 or obtained < 0 or obtained > maximum: raise ValueError
    except ValueError:
        print("Enter valid marks (obtained must be between 0 and maximum)."); return
    exam_date = input("Exam date YYYY-MM-DD (optional): ").strip()
    if exam_date:
        try: exam_date = date.fromisoformat(exam_date).isoformat()
        except ValueError:
            print("Invalid date."); return
    else: exam_date = None
    try:
        with db() as c:
            c.execute("""INSERT INTO marks(student_id,subject,exam,obtained,maximum,exam_date)
                         VALUES(?,?,?,?,?,?)""",(sid,subject,exam,obtained,maximum,exam_date))
        print("Marks saved.")
    except sqlite3.IntegrityError:
        print("Marks for this subject and exam already exist for this student.")

def record_attendance():
    sid = ask("Student ID: ")
    if not exists(sid):
        print("Student not found. Add student first."); return
    day = valid_date("Date YYYY-MM-DD: ")
    choice = input("Status: P=Present, A=Absent, L=Late: ").strip().upper()
    status = {"P":"Present","A":"Absent","L":"Late"}.get(choice)
    if not status:
        print("Choose P, A, or L."); return
    with db() as c:
        c.execute("""INSERT INTO attendance(student_id,attendance_date,status)
            VALUES(?,?,?) ON CONFLICT(student_id,attendance_date)
            DO UPDATE SET status=excluded.status""",(sid,day,status))
    print("Attendance saved. Re-entering a date updates its status.")

def attendance_report():
    sid = ask("Student ID: ")
    with db() as c:
        s = c.execute("SELECT name FROM students WHERE student_id=?", (sid,)).fetchone()
        rows = c.execute("""SELECT attendance_date,status FROM attendance
                            WHERE student_id=? ORDER BY attendance_date DESC""",(sid,)).fetchall()
    if not s:
        print("Student not found."); return
    print(f"\\nAttendance for {s['name']} ({sid})")
    if not rows:
        print("No attendance records."); return
    for r in rows: print(r["attendance_date"], "-", r["status"])
    p = sum(r["status"]=="Present" for r in rows)
    a = sum(r["status"]=="Absent" for r in rows)
    l = sum(r["status"]=="Late" for r in rows)
    print(f"Present: {p} | Absent: {a} | Late: {l}")
    print(f"Attendance percentage (Present + Late): {(p+l)/len(rows)*100:.2f}%")

def main():
    setup()
    actions = {
        "1":("Add student",add_student),
        "2":("View all students",list_students),
        "3":("View complete student profile",view_student),
        "4":("Update student details",update_student),
        "5":("Delete student",delete_student),
        "6":("Add marks",add_marks),
        "7":("Record attendance",record_attendance),
        "8":("View attendance report",attendance_report),
    }
    while True:
        print("\\n===== STUDENT DATABASE MANAGEMENT SYSTEM =====")
        for key,(label,_) in actions.items(): print(f"{key}. {label}")
        print("9. Exit")
        choice = input("Choose (1-9): ").strip()
        if choice == "9":
            print("Database saved. Goodbye!"); break
        if choice in actions:
            try: actions[choice][1]()
            except sqlite3.Error as e: print("Database error:",e)
        else: print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
