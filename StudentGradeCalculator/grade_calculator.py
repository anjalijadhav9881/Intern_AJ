"""
Project: Student Grade Calculator
Description: An interactive command-line application that validates student marks,
             computes grades using conditional logic, and provides encouraging feedback.
"""

def calculate_grade(marks):
    """Determines the letter grade and encouraging message based on marks."""
    if 90 <= marks <= 100:
        return "A", "Outstanding! You crushed it! "
    elif 80 <= marks <= 89:
        return "B", "Very Good! Keep it up! "
    elif 70 <= marks <= 79:
        return "C", "Good effort! Room for improvement. "
    elif 60 <= marks <= 69:
        return "D", "Passed. Let's work harder next time! "
    else:
        return "F", "Don't give up! Review the concepts and try again. "

def get_valid_marks():
    """Continuously prompts the user until a valid integer between 0 and 100 is entered."""
    while True:
        try:
            marks = int(input("Enter marks (0-100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print(" Invalid range! Marks must be between 0 and 100. Try again.")
        except ValueError:
            print(" Invalid input! Please enter a numerical integer value.")

def main():
    print("        STUDENT GRADE CALCULATOR UTILITY        ")
    print("=" * 45 + "\n")

    # Get student name
    name = input("Enter student name: ").strip()
    if not name:
        name = "Student"

    # Get verified marks using our loop mechanism
    marks = get_valid_marks()

    # Calculate grade and retrieve matching message
    grade, message = calculate_grade(marks)

    # Display results cleanly formatted
    print("\n" + "~" * 45)
    print(f" RESULT FOR {name.upper()}:")
    print(f"Marks: {marks}/100")
    print(f"Grade: {grade}")
    print(f"Message: {message}")
    print("~" * 45)

if __name__ == "__main__":
    main()