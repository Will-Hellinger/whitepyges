import pytest
from unittest.mock import patch, MagicMock
from whitepyges.phone import Phone
from whitepyges import helper, config


def test_phone_initialization():
    phone = Phone("123-456-7890")
    assert phone.phone_number == helper.format_phone_number("123-456-7890")
    assert phone.headers == config.HEADERS


def test_phone_initialization_invalid_number():
    with pytest.raises(ValueError, match="Phone number is required"):
        Phone("")


@patch("whitepyges.helper.make_request_with_retries")
@patch("whitepyges.helper.get_endpoint")
def test_phone_search(mock_get_endpoint, mock_make_request):
    mock_get_endpoint.return_value = "mock_url"
    mock_response = MagicMock()
    mock_response.text = """
    <html>
        <div data-qa-selector="phone-header-area-code-info">
            About their location and providerTexasArea code locationAustin,Round Rock,San Marcos,Georgetown,Cedar ParkOther major (512) citiesT-Mobile USA, Inc.Phone carrier informationMore on their Area CodeT-Mobile USA, Inc. is the primary carrier for +1 (512) 591-7315.
        </div>
        <a class="wp-chip">Spam info available</a>
    </html>
    """
    mock_make_request.return_value = mock_response

    phone = Phone("123-456-7890")
    result = phone.search()

    assert result["spam_info"] == "Spam info available"
    assert result["state"] == "Texas"
    assert result["cities"] == "Austin,Round Rock,San Marcos,Georgetown,Cedar Park"
    assert result["area_code"] == "123"
    assert result["url"] == "mock_url"


@patch("whitepyges.helper.make_request_with_retries")
@patch("whitepyges.helper.get_endpoint")
def test_phone_search_no_results(mock_get_endpoint, mock_make_request):
    mock_get_endpoint.return_value = "mock_url"
    mock_response = MagicMock()
    mock_response.text = "<html></html>"
    mock_make_request.return_value = mock_response

    phone = Phone("123-456-7890")
    result = phone.search()

    assert result is None


def test_phone_repr():
    phone = Phone("123-456-7890")
    assert repr(phone) == helper.format_repr(phone)


def test_phone_str():
    phone = Phone("123-456-7890")
    assert str(phone) == helper.format_str(phone)
