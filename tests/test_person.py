import pytest
from unittest.mock import patch, MagicMock
from whitepyges.person import Person
from whitepyges import helper, config


def test_person_initialization():
    person = Person("John", "Doe", 30, "New York", "NY", "10001")
    assert person.name == helper.format_name("John", "Doe")
    assert person.age == helper.format_age(30)
    assert person.location == helper.format_location("New York", "NY", "10001")
    assert person.headers == config.HEADERS


def test_person_initialization_invalid_name():
    with pytest.raises(ValueError, match="First name and last name are required"):
        Person("", "Doe")
    with pytest.raises(ValueError, match="First name and last name must be strings"):
        Person(123, "Doe")


@patch("whitepyges.helper.make_request_with_retries")
@patch("whitepyges.helper.get_endpoint")
def test_person_search(mock_get_endpoint, mock_make_request):
    mock_get_endpoint.return_value = "mock_url"
    mock_response = MagicMock()
    mock_response.text = """
    <html>
        <script type="application/ld+json">
        [{"itemListElement": [{"@type": "ListItem", "item": {"@type": "Person", "name": "John Doe", "description": "John Doe in their 30s", "url": "/profile"}}]}]
        </script>
    </html>
    """
    mock_make_request.return_value = mock_response

    person = Person("John", "Doe", 30)
    results = person.search()

    assert len(results) == 1
    assert results[0]["name"] == "John Doe"
    assert results[0]["url"] == config.BASE_URL + "/profile"


@patch("whitepyges.helper.make_request_with_retries")
@patch("whitepyges.helper.get_endpoint")
def test_person_search_no_results(mock_get_endpoint, mock_make_request):
    mock_get_endpoint.return_value = "mock_url"
    mock_response = MagicMock()
    mock_response.text = "<html></html>"
    mock_make_request.return_value = mock_response

    person = Person("John", "Doe", 30)
    results = person.search()

    assert results is None


def test_clean_person_data():
    person = Person("John", "Doe", 30)
    raw_data = {
        "itemListElement": [
            {
                "@type": "ListItem",
                "item": {
                    "@type": "Person",
                    "name": "John Doe",
                    "description": "John Doe in their 30s",
                    "url": "/profile",
                },
            },
            {
                "@type": "ListItem",
                "item": {
                    "@type": "Person",
                    "name": "Jane Doe",
                    "description": "Jane Doe in their 40s",
                    "url": "/profile2",
                },
            },
        ]
    }
    cleaned_data = person._clean_person_data(raw_data, "30")
    assert len(cleaned_data) == 1
    assert cleaned_data[0]["name"] == "John Doe"
    assert cleaned_data[0]["url"] == config.BASE_URL + "/profile"


def test_person_repr():
    person = Person("John", "Doe", 30)
    assert repr(person) == helper.format_repr(person)


def test_person_str():
    person = Person("John", "Doe", 30)
    assert str(person) == helper.format_str(person)
