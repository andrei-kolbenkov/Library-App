import json
import os
import time
from typing import List, Dict, Optional


# Класс книги
class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "В наличии") -> None:
        """
        Инициализирует объект книги.
        :param id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги ("В наличии" или "Выдана").
        """
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, str | int]:
        """
        Преобразует объект книги в словарь.
        :return: Словарь с данными книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


# Класс библиотеки
class Library:
    def __init__(self, data_file: str = "library.json") -> None:
        """
        Инициализирует объект библиотеки.
        :param data_file: Путь к файлу, где хранятся данные о книгах.
        """
        self.data_file: str = data_file
        self.books: List[Book] = []
        self.next_id: int = 1  # Следующий уникальный ID
        self.load_books()

    def load_books(self) -> None:
        """Загружает книги из файла."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as file:
                    books_data: List[Dict[str, str | int]] = json.load(file)
                    self.books = [Book(**data) for data in books_data]
                    # Установим next_id как максимальный id + 1
                    if self.books:
                        self.next_id = max(book.id for book in self.books) + 1
            except json.JSONDecodeError:
                print("Ошибка загрузки данных, файл поврежден.")
        else:
            self.books = []

    def save_books(self) -> None:
        """Сохраняет книги в файл."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            # Записывает данные в формате JSON в указанный файл.
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Добавляет новую книгу в библиотеку.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания.
        """
        new_book: Book = Book(self.next_id, title, author, year)
        self.books.append(new_book)
        self.next_id += 1
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id: int) -> None:
        """
        Удаляет книгу по ID.
        :param book_id: ID книги.
        """
        # book будет либо объектом класса Book, либо None.
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID '{book_id}' удалена.")
        else:
            print(f"Книга с ID '{book_id}' не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Ищет книгу по ID.
        :param book_id: ID книги.
        :return: Найденная книга или None.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(self, keyword: str) -> None:
        """
        Ищет книги по ключевому слову.
        :param keyword: Ключевое слово для поиска.
        """
        results: List[Book] = [
            book for book in self.books
            if keyword.lower() in book.title.lower() or
               keyword.lower() in book.author.lower() or
               keyword.lower() in str(book.year)
        ]
        if results:
            self.display_books(results)
        else:
            print("Книги не найдены.")

    def display_books(self, books: Optional[List[Book]] = None) -> None:
        """
        Отображает книги.
        :param books: Список книг для отображения. Если None, отображаются все книги.
        """
        books = books if books else self.books
        # Регулирование отступов между колонками
        id_length: int = 10
        title_length: int = 50
        author_length: int = 30
        year_length: int = 10
        status_length: int = 10
        if books:
            print(f"{'ID':<{id_length}}{'НАЗВАНИЕ':<{title_length}}{'АВТОР':<{author_length}}{'ГОД':<{year_length}}{'СТАТУС':<{status_length}}")
            print("="*(id_length + title_length + author_length + year_length + status_length))
            for book in books:
                print(f"{book.id:<{id_length}}{book.title:<{title_length}}{book.author:<{author_length}}{book.year:<{year_length}}{book.status:<{status_length}}")
        else:
            print("Библиотека пуста...")

    def update_book_status(self, book_id: int) -> None:
        """
        Обновляет статус книги.
        :param book_id: ID книги.
        """
        book: Optional[Book] = self.find_book_by_id(book_id)
        if book:
            choice_status: Dict[int, str] = {1: "В наличии", 2: "Выдана"}
            status_mes: str = "\n".join(f"{key}. {value} " for key, value in choice_status.items())
            new_status: str = input(f"Выберите новый статус: \n{status_mes}").strip()
            while new_status not in str(choice_status.keys()):
                print("Неверный ввод")
                new_status = input(f"Выберите новый статус: \n{status_mes}").strip()
            else:
                book.status = choice_status[int(new_status)]
                self.save_books()
                print(f"Статус книги '{book.title}' с ID '{book_id}' изменен на '{choice_status[int(new_status)]}'.")
        else:
            print(f"Книга с ID '{book_id}' не найдена.")


# Главная функция
def main() -> None:
    """
    Запускает программу библиотеки.
    """
    library: Library = Library()

    print("Добро пожаловать в каталог библиотеки!")

    while True:
        print("\nДоступные команды:")
        print("1. Отобразить все книги")
        print("2. Добавить книгу")
        print("3. Удалить книгу")
        print("4. Искать книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice: str = input("Выберите действие: ").strip()

        if choice == "1":
            library.display_books()

        elif choice == "2":
            title: str = input("Введите название книги: ").strip()
            author: str = input("Введите автора книги: ").strip()
            year: str = input("Введите год издания книги: ").strip()
            while (not year.isdigit()) or (len(year) > 4):
                print("Год может быть 4-х значным числом и меньше.")
                year = input("Введите год издания книги: ").strip()
            else:
                library.add_book(title, author, int(year))

        elif choice == "3":
            book_id: str = input("Введите ID книги для удаления: ").strip()
            if book_id.isdigit():
                library.remove_book(int(book_id))
            else:
                print("ID должен быть числом.")

        elif choice == "4":
            keyword: str = input("Введите ключевое слово для поиска: ").strip()
            library.search_books(keyword)

        elif choice == "5":
            book_id: str = input("Введите ID книги: ").strip()
            while not book_id.isdigit():
                print("ID должен быть числом.")
                book_id = input("Введите ID книги: ").strip()
            else:
                library.update_book_status(int(book_id))

        elif choice == "6":
            print("Выход из программы...")
            time.sleep(1)
            break

        else:
            print("Некорректный ввод. Повторите попытку.")


if __name__ == "__main__":
    main()
