import click

from packages.IS_Tester import check_daily


def welcome():
    print("══════════════════════════════════════════════")
    print("✨ Welcome to Foolad Sang Automation App ✨")
    print("This application provides multiple powerful features to assist you.")
    print("Available features:")
    print(
        " • Tester : Verify the accuracy and consistency of the daily production report."
    )
    print("══════════════════════════════════════════════")


def get_command():
    commands = {
        "tester": "Check the accuracy of the daily production report",
        "analyze": "Analyze text data and provide insights",
        "calculate": "Perform numeric calculations (e.g., square a number)",
        "exit": "Close the application",
    }

    print("\n══════════════════════════════════════════════")
    print("✨ Available Commands ✨")
    for cmd, desc in commands.items():
        print(f" • {cmd:<10} : {desc}")
    print("══════════════════════════════════════════════")

    command = input("Please enter your command: ").strip().lower()
    return command


def tester():
    try:
        # این روش اجرای برنامه برای این است که به محض تمام شدن تابع کل برنامه بسته نشود
        check_daily.main(standalone_mode=False)
    except Exception as e:
        print("══════════════════════════════════════════════")
        print("⚠️  An unexpected error occurred while running the Tester feature.")
        print(f"   Details: {e}")
        print("   Please check your input or file and try again.")
        print("══════════════════════════════════════════════")
        return


def main():
    while True:
        command = get_command()

        if command == "tester":
            tester()
        elif command == "exit":
            print("Program closed successfully. Goodbye! 🌙")
            break
        else:
            print("⚠️ Unknown command. Please try again.")
            continue


if __name__ == '__main__':
    welcome()
    main()
