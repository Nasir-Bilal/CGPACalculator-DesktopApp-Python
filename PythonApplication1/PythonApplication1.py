import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class Course:
    def __init__(self, name, obtainGrade, gradePoints, creditHrs, totalPoints):
        self.name = name
        self.obtainGrade = obtainGrade
        self.gradePoints = gradePoints
        self.creditHrs = creditHrs
        self.totalPoints = totalPoints
        
    def display(self):
        print(f"Name: {self.name}")
        print(f"obtainGrade: {self.obtainGrade}")
        print(f"Grade Point: {self.gradePoints}")
        print(f"Credit Hours: {self.creditHrs}")
        print(f"Sum: {self.totalPoints}")

def increment_value():
    try:
        current_val = int(entry_nCourses.get())
    except ValueError:
        current_val = 0
        
    new_value = min(current_val + 1, 10)
    entry_nCourses.delete(0, tk.END)
    entry_nCourses.insert(0, str(new_value))
    update_input_fields() 

def decrement_value():
    try:
        current_val = int(entry_nCourses.get())
    except ValueError:
        current_val = 0
    new_value = max(current_val - 1, 0)
    entry_nCourses.delete(0, tk.END)
    entry_nCourses.insert(0, str(new_value))
    update_input_fields() 

def selectGrade(grade):
    grades = {
        "A+": 4.0, "A": 4.0, "-A": 3.67, "B+": 3.33, "B": 3.0,
        "-B": 2.67, "C+": 2.33, "C": 2.0, "-C": 1.67, "D+": 1.33,
        "D": 1.0, "F": 0.0
    }
    return grades.get(grade, 0.0)

def calculateGPA(courses):
    total_points = sum(course.totalPoints for course in courses)
    total_credits = sum(course.creditHrs for course in courses)
    return float(total_points / total_credits) if total_credits else 0.0

def performCalculation():
    courses = []

    try:
        nCourses = int(entry_nCourses.get())
    except ValueError:
        nCourses = 0

    for i in range(nCourses):
        name = entries_name[i].get() or "default"
        creditHrs = int(entries_credits[i].get() or 1)
        obtainGrade = entries_grade[i].get() or "F"

        gradePoints = float(selectGrade(obtainGrade))
        totalPoints = creditHrs * gradePoints
        
        course = Course(name, obtainGrade, gradePoints, creditHrs, totalPoints)
        course.display()
        courses.append(course)

    s_gpa = calculateGPA(courses)
    
    try:
        c_gpa = float(entry_CGPA.get())
    except ValueError:
        c_gpa = 0.0
    
    try:
        semester_no = int(semester_num.get())
    except ValueError:
        semester_no = 0
   
    new_c_gpa = (s_gpa + (c_gpa * semester_no)) / (semester_no + 1)
  
    # Update results with a small delay to avoid UI lag
    update_results(s_gpa, new_c_gpa)

def update_results(s_gpa, new_c_gpa):
    label_sgpa.config(text=f"{s_gpa:.2f}")
    label_cgpa.config(text=f"{new_c_gpa:.2f}")

def validate_positive_number(action, value_if_allowed):
    # Only allow positive numbers (no negative or decimal points)
    if action == '1':  # If inserting something
        if value_if_allowed.isdigit() and int(value_if_allowed) > 0:
            return True
        else:
            return False
    else:
        return True

def update_input_fields():
    try:
        nCourses = int(entry_nCourses.get())
    except ValueError:
        nCourses = 0

    # Clear existing widgets
    for widget in dynamic_frame.winfo_children():
        widget.grid_forget()

    # Create headers
    ttk.Label(dynamic_frame, text="sr.", font=("Arial", 10),
             width=6).grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(dynamic_frame, text="Name", font=("Arial", 10),
             width=20).grid(row=1, column=1, padx=10, pady=10)
    ttk.Label(dynamic_frame, text="Credits", font=("Arial", 10),
             width=8).grid(row=1, column=2, padx=10, pady=10)
    ttk.Label(dynamic_frame, text="Grade", font=("Arial", 10),
             width=8).grid(row=1, column=3, padx=10, pady=10)

    global entries_name, entries_grade, entries_credits
    entries_name = []
    entries_grade = []
    entries_credits = []

    for i in range(nCourses):
        ttk.Label(dynamic_frame, text=f"{i+1}.",
                 font=("Arial", 10)).grid(row=i+2, column=0, padx=10, pady=10)
        
        entry_name = ttk.Entry(dynamic_frame, width=20)
        entry_name.grid(row=i+2, column=1, padx=10, pady=10)
        entries_name.append(entry_name)

        # Add validation to allow only positive numbers for credits
        vcmd = (window.register(validate_positive_number), '%d', '%P')
        entry_credits = ttk.Entry(dynamic_frame, width=8, validate='key', validatecommand=vcmd)
        entry_credits.grid(row=i+2, column=2, padx=10, pady=10)
        entries_credits.append(entry_credits)

        entry_grade = ttk.Combobox(dynamic_frame,
                                  values=["A+", "A", "-A", "B+", "B", "-B", "C+", "C", "-C", "D+", "D", "F"],
                                 font=("Arial", 10), width=5)
        entry_grade.grid(row=i+2, column=3, padx=10, pady=10)
        entries_grade.append(entry_grade)

def clear_fields():
    entry_nCourses.delete(0, tk.END)
    
    for entry in entries_name:
        entry.delete(0, tk.END)
    for entry in entries_credits:
        entry.delete(0, tk.END)
    for entry in entries_grade:
        entry.set('')  # Use set() for Combobox
    
    entry_CGPA.delete(0, tk.END)
    semester_num.set('')
    
    label_sgpa.config(text="")
    label_cgpa.config(text="")
    
    update_input_fields()

window = ThemedTk(theme="arc")
window.title("GPA Calculator")
window.geometry("700x615+40+40")
window.resizable(False, False)
window.configure(bg='#f5f6f8')


# Configure grid row and column weights
window.grid_rowconfigure(3, weight=1)  # Make sure row 3 expands
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_columnconfigure(4, weight=1)
window.grid_columnconfigure(5, weight=0)

ttk.Label(window, text="Number of Courses", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')

entry_nCourses = ttk.Entry(window, width=10)
entry_nCourses.grid(row=0, column=1, padx=10, pady=10)
ttk.Button(window, text="+", width=2,
          command=increment_value).grid(row=0, column=2, padx=0, pady=10)
ttk.Button(window, text="-", width=3,
          command=decrement_value).grid(row=0, column=3, padx=0, pady=10)

ttk.Button(window, text="Calculate GPA", width=15,
          command=performCalculation).grid(row=0, column=4, padx=5, pady=10)
ttk.Button(window, text="Clear", width=15,
          command=clear_fields).grid(row=0, column=5, padx=5, pady=10)

ttk.Label(window, text="Current CGPA",
         font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_CGPA = ttk.Entry(window, width=10)
entry_CGPA.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(window, text="Semester Completed", 
          font=("Arial", 10)).grid(row=2, column=2, padx=10, pady=10, sticky='e')
semester_num = ttk.Combobox(window, 
                            values=[str(i) for i in range(1, 9)], font=("Arial", 10), width=5)
semester_num.grid(row=2, column=4, padx=5, pady=10)

dynamic_frame = ttk.Frame(window)
dynamic_frame.grid(row=3, column=0, columnspan=5, pady=10, sticky='nsew')

results_frame = ttk.Frame(window, borderwidth=1, relief="raised")
results_frame.grid(row=1, column=5, rowspan=3, padx=10, pady=10, sticky='n')

# Create labels within the results frame only once
ttk.Label(results_frame, text="Result", 
          font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
ttk.Label(results_frame, text="SGPA",
         font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
ttk.Label(results_frame, text="CGPA",
         font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky='w')

label_sgpa = ttk.Label(results_frame, text="", font=("Arial", 12), width=10)
label_sgpa.grid(row=1, column=1, padx=10, pady=5, sticky='w')

label_cgpa = ttk.Label(results_frame, text="", font=("Arial", 12), width=10)
label_cgpa.grid(row=2, column=1, padx=10, pady=5, sticky='w')

window.mainloop()
