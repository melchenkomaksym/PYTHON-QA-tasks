import pytest
import requests
from assertpy import assert_that

BASE_URL = "http://localhost:5000/v1/books"


@pytest.fixture(scope="class")
def setup_teardown():
    print("Setting up before tests")
    yield
    print("Tearing down after tests")


class TestBookAPI:

    @pytest.mark.parametrize("book_type, title", [
        ("Science", "Book One"),
        ("Adventure", "Book Two"),
        ("Romance", "Love Story")
    ])
    def test_add_book(self, setup_teardown, book_type, title):
        payload = {"type": book_type, "title": title}
        response = requests.post(f"{BASE_URL}/manipulation", json=payload)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()["type"]).is_equal_to(book_type)
        assert_that(response.json()["title"]).is_equal_to(title)

    def test_get_books_invalid_type(self, setup_teardown):
        response = requests.get(f"{BASE_URL}/ids?book_type=InvalidType")
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()["message"]).contains("The book entity is not valid")

    @pytest.mark.parametrize("book_type", ["Science", "Adventure"])
    def test_get_books_by_type(self, setup_teardown, book_type):
        response = requests.get(f"{BASE_URL}/ids?book_type={book_type}")
        assert_that(response.status_code).is_equal_to(200)
        if len(response.json()) > 0:
            assert_that(response.json()[0]["type"]).is_equal_to(book_type)

    def test_delete_invalid_book(self, setup_teardown):
        response = requests.delete(f"{BASE_URL}/manipulation?id=invalid_id")
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()["message"]).contains("There is no such book")

    def test_update_book_invalid_id(self, setup_teardown):
        payload = {"title": "Updated Title"}
        response = requests.put(f"{BASE_URL}/manipulation?id=invalid_id", json=payload)
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()["message"]).contains("There is no such book")

    def test_get_latest_books(self, setup_teardown):
        response = requests.get(f"{BASE_URL}/latest?limit=2")
        assert_that(response.status_code).is_equal_to(200)
        assert_that(len(response.json())).is_less_than_or_equal_to(2)

    def test_get_latest_books_invalid_limit(self, setup_teardown):
        response = requests.get(f"{BASE_URL}/latest?limit=-1")
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()["message"]).contains("The request is not valid")

    def test_get_book_info_invalid_id(self, setup_teardown):
        response = requests.get(f"{BASE_URL}/info?id=invalid_id")
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()["message"]).contains("There is no such book")

    def test_add_book_without_title(self, setup_teardown):
        payload = {"type": "Science"}
        response = requests.post(f"{BASE_URL}/manipulation", json=payload)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()["message"]).contains("The request is not valid")

    def test_add_book_without_type(self, setup_teardown):
        payload = {"title": "Book Without Type"}
        response = requests.post(f"{BASE_URL}/manipulation", json=payload)
        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()["message"]).contains("The request is not valid")
