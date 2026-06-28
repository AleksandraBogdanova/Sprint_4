import pytest
from main import BooksCollector

# --- Тесты для метода add_new_book ---

@pytest.mark.parametrize(
    "book_name, should_be_added",
    [
        ("Властелин колец", True),
        ("Книга с длинным, но допустимым названием", True),
        ("А" * 41, False)
    ],
    ids=[
        "Валидное имя добавляется",
        "Длинное валидное имя добавляется",
        "Слишком длинное имя не добавляется",
    ]
)
def test_add_new_book_validates_name(book_name, should_be_added):
    """
    Проверяет, что метод add_new_book корректно валидирует имена книг.
    Валидные имена добавляются, невалидные — нет.
    """
    collector = BooksCollector()
    collector.add_new_book(book_name)

    if should_be_added:
        assert book_name in collector.books_genre
    else:
        assert book_name not in collector.books_genre

def test_duplicate_book_not_added():
    """Проверяет, что добавление книги с уже существующим именем не создает дубликат."""
    collector = BooksCollector()
    book_name = 'Книга1'

    collector.add_new_book(book_name)
    initial_count = len(collector.books_genre)

    collector.add_new_book(book_name)

    assert len(collector.books_genre) == initial_count

# --- Тесты для метода set_book_genre ---

@pytest.mark.parametrize(
    "genre_to_set, expected_stored_genre",
    [
        ("Фантастика", "Фантастика"), 
        ("фантастика", ""),           
        ("", ""),                     
        ("Романтика", ""),            
    ],
    ids=[
        "Жанр из списка self.genres устанавливается",
        "Жанр не из списка self.genres (чувствительность к регистру) игнорируется",
        "Пустой жанр устанавливается",
        "Недопустимый жанр игнорируется",
    ]
)
def test_set_book_genre_stores_value(genre_to_set, expected_stored_genre):
    """Проверяет, что set_book_genre сохраняет только допустимые жанры из списка self.genres."""
    collector = BooksCollector()
    book_name = "Книга1"
    collector.add_new_book(book_name)

    collector.set_book_genre(book_name, genre_to_set)

    assert collector.books_genre[book_name] == expected_stored_genre

def test_set_book_genre_for_non_existing_book():
    """Проверяет, что установка жанра для несуществующей книги не вызывает ошибок."""
    collector = BooksCollector()

    collector.set_book_genre("Несуществующая книга", "Фантастика")


    assert len(collector.books_genre) == 0

# --- Тесты для метода get_book_genre ---

def test_get_book_genre_returns_value_for_existing_book():
    """Проверяет, что get_book_genre возвращает жанр для существующей книги."""
    collector = BooksCollector()
    book_name = "Книга1"

    collector.add_new_book(book_name)
    collector.books_genre[book_name] = "Фантастика" 

    assert collector.get_book_genre(book_name) == "Фантастика"

def test_get_book_genre_returns_none_for_non_existing_book():
    """Проверяет, что get_book_genre возвращает None для несуществующей книги."""
    collector = BooksCollector()

    result = collector.get_book_genre("Несуществующая книга")

    assert result is None

# --- Тесты для метода get_books_with_specific_genre ---

def test_get_books_with_specific_genre_filters_correctly():
    """Проверяет, что метод возвращает только книги с указанным жанром."""
    collector = BooksCollector()

    book1, book2, book3 = "Книга1", "Книга2", "Книга3"

    collector.add_new_book(book1)
    collector.add_new_book(book2)
    collector.add_new_book(book3)

    collector.books_genre[book1] = "Фантастика"
    collector.books_genre[book2] = "Фантастика"

    result = collector.get_books_with_specific_genre("Фантастика")

    assert set(result) == {book1, book2}

# --- Тесты для избранного (favorites) ---

def test_favorites_operations():
     """Проверяет добавление и удаление книги из избранного."""
     collector = BooksCollector()
     book_name = 'Книга1'
 
     collector.add_new_book(book_name)
 
     collector.add_book_in_favorites(book_name)
     assert book_name in collector.get_list_of_favorites_books()
 
     collector.delete_book_from_favorites(book_name)
     assert book_name not in collector.get_list_of_favorites_books()
 
def test_add_non_existing_book_to_favorites():
     """Проверяет, что добавление несуществующей книги в избранное не вызывает ошибок."""
     collector = BooksCollector()

     collector.add_book_in_favorites('Несуществующая книга')

     favorites = collector.get_list_of_favorites_books()
     assert 'Несуществующая книга' not in favorites


def test_get_list_of_favorites_books_returns_current_favorites():
     """Проверяет, что get_list_of_favorites_books возвращает актуальный список избранного."""
     collector = BooksCollector()
     book1, book2 = "Книга1", "Книга2"
 
     collector.add_new_book(book1)
     collector.add_new_book(book2)
     
     collector.add_book_in_favorites(book1)
 
     favorites = collector.get_list_of_favorites_books()
 
     assert set(favorites) == {book1}
 
def test_get_books_genre_returns_current_state():
     """Проверяет, что get_books_genre возвращает актуальное состояние словаря жанров."""
     collector = BooksCollector()
     book1, book2 = "Книга1", "Книга2"
 
     collector.add_new_book(book1)
     collector.add_new_book(book2)
     
     expected_state = {book1: "Фантастика", book2: "Комедия"}
     collector.books_genre.update(expected_state) 

     result = collector.get_books_genre()
 
     assert result == expected_state


@pytest.mark.parametrize(
   "genre, should_be_included",
   [
       ("Мультфильмы", True),
       ("Комедии", True),
       ("Ужасы", False),
       ("Детективы", False),
       ("Фантастика", True),  
   ],
   ids=[
       "Жанр 'Мультфильмы' включается",
       "Жанр 'Комедии' включается",
       "Жанр 'Ужасы' исключается",
       "Жанр 'Детективы' исключается",
       "Жанр 'Фантастика' включается",
   ]
)
def test_get_books_for_children_includes_and_excludes_genres(genre, should_be_included):
   """
   Проверяет, что метод get_books_for_children включает книги с детскими жанрами
   и исключает книги с недетскими.
   """
   collector = BooksCollector()
   
   book_name = f"Книга ({genre})"
   
   collector.add_new_book(book_name)
   collector.set_book_genre(book_name, genre)
   
   children_books = collector.get_books_for_children()
   
   if should_be_included:
      assert book_name in children_books, f"Книга с жанром '{genre}' должна быть в детском списке"
   else:
      assert book_name not in children_books, f"Книга с жанром '{genre}' НЕ должна быть в детском списке"