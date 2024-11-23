class Book:
    """
    Класс для представления книги.

    Методы:
        to_string():
            Преобразует объект Book в строковое представление
        from_string():
            Создает экземпляр класса книги из строки.
    """
    def __init__(self, book_id: int, title: str, author: str,
                 year: int, status: str = "в наличии") -> None:
        """
        Инициализирует объект класса Book.

        Аргументы:
            book_id: id книги.
            title: Название книги.
            author: Автор книги.
            year: Год издания.
            status: Статус книги.
        """
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_string(self) -> str:
        """
        Преобразует объект Book в строковое представление.

        Возвращает:
            str: строка, содержащая сведения о книге в формате
                "идентификатор; название; автор; год; статус".
        """
        return f"{self.id};{self.title};{self.author};{self.year};{self.status}"

    @classmethod
    def from_string(cls, string: str) -> 'Book':
        """
        Создает экземпляр класса книги из строки.

        Возвращает:
            Book: Экземпляр класса Book.
        """
        parts: list = string.strip().split(";")
        return cls(int(parts[0]), parts[1], parts[2], int(parts[3]), parts[4])


class Library:
    """
    Класс для управления библиотекой.

    Этот класс позволяет добавлять, удалять, искать книги,
    а также обновлять их статус.

    Методы:
        load_data():
            Загружает данные библиотеки из файла.
        save_data():
            Сохраняет текущие данные библиотеки в файл.
        add_book():
            Добавляет новую книгу в библиотеку.
        generate_id():
            Генерирует id для добавляемой книги.
        delete_book():
            Удаляет книгу по её ID.
        search_books():
            Находит книги в библиотеке.
        display_books():
            Отображает все книги из библиотеки.
        update_status():
            Изменяет статус книги.
        main():
            Запускает приложение и меню.
    """
    def __init__(self, data_file: str = "library.txt") -> None:
        """
        Инициализирует объект класса Library.

        Аргументы:
            books (list[Book]): Список объектов класса Book,
            представляющих книги в библиотеке.
            data_file (str): Имя файла для сохранения данных библиотеки.
        """
        self.data_file: str = data_file
        self.books: list = self.load_data()

    def load_data(self) -> list:
        """
        Загружает книги из текстового файла.

        Исключения:
            FileNotFoundError: Если не найден файл.
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                books = [Book.from_string(line) for line in file]

            return sorted(books, key=lambda b: b.id)

        except FileNotFoundError:
            return []

    def save_data(self) -> None:
        """Сохраняет книги в текстовый файл."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            for book in sorted(self.books, key=lambda b: b.id):
                file.write(book.to_string() + "\n")

    def add_book(self) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Исключения:
            ValueError: Если вводимое значение года не число.
        """
        title: str = input("Введите название книги: ").strip()
        author: str = input("Введите автора книги: ").strip()

        try:
            year: int = int(input("Введите год издания: ").strip())
        except ValueError:
            print("Ошибка: год должен быть числом!")
            return

        new_book = Book(self.generate_id(), title, author, year)
        self.books.append(new_book)
        self.books.sort(key=lambda b: b.id)

        self.save_data()
        print("Книга успешно добавлена!")

    def generate_id(self) -> int:
        """Генерирует id для добавляемой книги."""
        used_ids: set[int] = {book.id for book in self.books}
        new_id: int = 1
        while new_id in used_ids:
            new_id += 1

        return new_id

    def delete_book(self) -> None:
        """
        Удаляет книгу из библиотеки по её id.

        Исключения:
            ValueError: Если вводимое значение не число.
        """
        try:
            book_id: int = int(input("Введите ID книги для удаления: ").strip())
        except ValueError:
            print("Ошибка: ID должен быть числом!")
            return

        book = next((book for book in self.books if book.id == book_id), None)

        if book:
            self.books.remove(book)
            self.save_data()
            print("Книга успешно удалена!")
        else:
            print("Книга с таким ID не найдена.")

    def search_books(self) -> None:
        """Находит книги в библиотеке."""
        query: str = (input("Введите название, автора или год для поиска: ")
                      .strip().lower())
        results: list = [
            book for book in self.books
            if query in book.title.lower()
            or query in book.author.lower()
            or query == str(book.year)
        ]

        if results:
            print("Найдены книги:")
            self.display_books(results)
        else:
            print("Книг по запросу не найдено.")

    def display_books(self, books=None) -> None:
        """Отображает все книги из библиотеки."""
        books: list = books or self.books

        if not books:
            print("Библиотека пуста.")
        else:
            print("-"*100)
            for book in books:
                print(
                    f"| ID: {book.id} | "
                    f"Название: {book.title}, Автор: {book.author}, "
                    f"Год: {book.year}, Статус: {book.status}"
                )

    def update_status(self) -> None:
        """
        Изменяет статус книги.

        Исключения:
            ValueError: Если вводимое значение не число.
        """
        try:
            book_id: int = (int(input("Введите ID книги для изменения статуса: ")
                                .strip()))
        except ValueError:
            print("Ошибка: ID должен быть числом!")
            return

        book: Book | None = (next((book for book in self.books
                                   if book.id == book_id), None))

        if book:
            print("1 - в наличии")
            print("2 - выдана")
            choice: str = input("Выберите новый статус (1-2): ").strip()

            if choice in ["1", "2"]:
                new_status: str = "в наличии" if choice == "1" else "выдана"

                if book.status == new_status:
                    print("Книга уже имеет данный статус.")
                else:
                    book.status = new_status
                    self.save_data()
                    print("Статус книги успешно обновлен!")
            else:
                print("Некорректный ввод.")
        else:
            print("Книга с таким ID не найдена.")


def main() -> None:
    """Основная функция для запуска приложения."""
    library = Library()

    while True:
        print("\n" + "-" * 11 + "МЕНЮ" + "-" * 11)
        print("1 - Добавить книгу")
        print("2 - Удалить книгу")
        print("3 - Искать книгу")
        print("4 - Отобразить все книги")
        print("5 - Изменить статус книги")
        print("6 - Выход")

        choice: str = input("Выберите действие (1-6): ").strip()
        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.delete_book()
        elif choice == "3":
            library.search_books()
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            library.update_status()
        elif choice == "6":
            print("Выход из приложения.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
