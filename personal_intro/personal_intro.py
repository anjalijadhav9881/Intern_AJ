"""
Project: Personal Introduction Program
Description: A beginner-friendly Python program that collects user details
             interactively and displays a customized welcome message.
"""

def main():
    print("=" * 40)
    print("      WELCOME TO THE INTRO GENERATOR      ")
    print("=" * 40 + "\n")

    # Step 1: Gather user information using input()
    name = input("What is your name? ").strip()
    
    # Using a loop or check to ensure age is entered as a number (good practice!)
    while True:
        try:
            age = int(input("How old are you? "))
            break
        except ValueError:
            print("Please enter a valid number for your age.")

    hobby = input("What is your favorite hobby? ").strip()
    city = input("Which city are you from? ").strip()

    # Step 2: Format and display the personalized welcome message
    print("\n" + "~" * 40)
    print(f" Welcome {name}! ")
    print(f"You are {age} years old, live in {city}, and love {hobby}.")
    print("~" * 40)
    print("Thanks for running your first Python program!")

if __name__ == "__main__":
    main()