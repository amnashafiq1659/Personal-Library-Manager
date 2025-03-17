import json
from rich.console import Console
from rich.prompt import Prompt

console = Console()

library_file = "library.txt"


def load_library():
    try:
        with open(library_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(library):
    with open(library_file, "w") as file:
        json.dump(library, file, indent=4)


def add_book(library):
    title = Prompt.ask("\n[italic #FFCF40]Enter the title of the book[/italic #FFCF40]")
    author = Prompt.ask("[italic #FFCF40]Enter the author of the book[/italic #FFCF40]")
    try:
        year = int(
            Prompt.ask(
                "[italic #FFCF40]Enter the publication year of the book[/italic #FFCF40]"
            )
        )
    except ValueError:
        console.print(
            "\nInvalid year. Please enter a valid integer.", style="bold #DC143C"
        )
        return
    genre = Prompt.ask("[italic #FFCF40]Enter the genre of the book[/italic #FFCF40]")
    read = (
        Prompt.ask(
            "[italic #FFCF40]Have you read this book? (yes/no)[/italic #FFCF40]"
        ).lower()
        == "yes"
    )

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read,
    }
    library.append(book)
    console.print(
        f"\nBook '{title}' by {author} added successfully.", style="bold #9400D3"
    )


def remove_book(library):
    title = Prompt.ask(
        "\n[italic #FFCF40]Enter the title of the book to remove[/italic #FFCF40]"
    )
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            console.print(
                f"\nBook '{title}' removed successfully.", style="bold #9400D3"
            )
            return
    console.print(f"\nBook '{title}' not found in the library.", style="bold #DC143C")


def edit_book(library):
    title = Prompt.ask(
        "\n[italic #FFCF40]Enter the title of the book to edit[/italic #FFCF40]"
    )
    console.print("\nLeave blank to keep the same value", style="italic #FF7518")
    for book in library:
        if book["title"].lower() == title.lower():
            console.print(f"\nEditing book: {book['title']}", style="bold #ff69b4")
            book["title"] = (
                Prompt.ask("\n[italic #FFCF40]Enter the new title[/italic #FFCF40]")
                or book["title"]
            )
            book["author"] = (
                Prompt.ask("[italic #FFCF40]Enter the new author[/italic #FFCF40]")
                or book["author"]
            )
            try:
                book["year"] = int(
                    Prompt.ask(
                        "[italic #FFCF40]Enter the new publication year[/italic #FFCF40]"
                    )
                    or book["year"]
                )
            except ValueError:
                console.print(
                    "Invalid year. Please enter a valid integer.",
                    style="bold #DC143C     ",
                )
            book["genre"] = (
                Prompt.ask("[italic #FFCF40]Enter the new genre[/italic #FFCF40]")
                or book["genre"]
            )
            book["read"] = (
                Prompt.ask(
                    "[italic #FFCF40]Enter the new read status (yes/no)[/italic #FFCF40]"
                ).lower()
                == "yes"
                or book["read"]
            )
            console.print(
                f"\nBook '{title}' updated successfully.", style="bold #9400D3"
            )
            return
    console.print(f"\nBook '{title}' not found in the library.", style="bold #DC143C")


def search_books(library):
    console.print("\nSearch By:", style="bold #77DD77")
    console.print("1. Title", style="italic #ff69b4")
    console.print("2. Author", style="italic #ff69b4")

    choice = Prompt.ask("\n[bold #77DD77]Enter your choice[/bold #77DD77]")
    if choice == "1":
        key = "title"
        value = Prompt.ask(
            "\n[italic #FFCF40]Enter the title to search for[/italic #FFCF40]"
        )
    elif choice == "2":
        key = "author"
        value = Prompt.ask(
            "\n[italic #FFCF40]Enter the author to search for[/italic #FFCF40]"
        )
    else:
        console.print("\nInvalid choice. Please try again.", style="bold #DC143C")
        return

    matches = [book for book in library if value.lower() in book[key].lower()]

    if matches:
        console.print(f"\nFound {len(matches)} matches:", style="italic #FF7518")
        for idx, book in enumerate(matches, 1):
            console.print(
                f"\n{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}",
                style="bold #9400D3",
            )
    else:
        console.print("\nBook not found.", style="bold #DC143C")


def display_books(library):
    if not library:
        console.print("\nLibrary is empty.", style="bold #DC143C")
        return

    console.print("\nLibrary:", style="italic #FF7518")
    for idx, book in enumerate(library, 1):
        console.print(
            f"\n{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}",
            style="bold #9400D3",
        )
    console.print()


def display_statistics(library):
    total_books = len(library)
    if total_books == 0:
        console.print("\nBooks not found in the library.", style="bold #DC143C")
        return

    read_count = sum(1 for book in library if book["read"])
    percentage_read = (read_count / total_books) * 100

    console.print(f"\nLibrary Statistics:", style="bold #FF7518")
    console.print(f"\nTotal books: {total_books}", style="italic #FFCF40")
    console.print(f"Books read: {read_count}", style="italic #FFCF40")
    console.print(f"Books not read: {total_books - read_count}", style="italic #FFCF40")
    console.print(
        f"Percentage of books read: {percentage_read:.2f}%", style="italic #FFCF40"
    )


def main():
    library = load_library()
    while True:
        console.print(
            "\n📚Welcome to Personal Library Manager📚",
            style="bold italic #87CEEB",
            justify="center",
        )
        console.print("1. Add Book", style="italic #ff69b4")
        console.print("2. Remove Book", style="italic #ff69b4")
        console.print("3. Search Book", style="italic #ff69b4")
        console.print("4. Edit Book", style="italic #ff69b4")
        console.print("5. Display all Books", style="italic #ff69b4")
        console.print("6. Display Statistics", style="italic #ff69b4")
        console.print("7. Exit", style="italic #ff69b4")

        choice = Prompt.ask("\n[bold #77DD77]Enter your choice[/bold #77DD77]")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_books(library)
        elif choice == "4":
            edit_book(library)
        elif choice == "5":
            display_books(library)
        elif choice == "6":
            display_statistics(library)
        elif choice == "7":
            console.print(
                "\nExiting the Library Manager...",
                style="bold #9400D3",
                justify="center",
            )
            save_library(library)
            break
        else:
            console.print(
                "\nInvalid choice. Please enter a valid option.", style="bold #DC143C"
            )


if __name__ == "__main__":
    main()
