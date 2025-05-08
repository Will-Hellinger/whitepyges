import pytest
from unittest.mock import patch, MagicMock

from whitepyges.address import Address
from whitepyges import helper, config


def test_address_initialization():
    with pytest.raises(ValueError, match="Street is required"):
        Address()

    with pytest.raises(ValueError, match="City is required"):
        Address(street="123 Main St")

    with pytest.raises(ValueError, match="State or zip code is required"):
        Address(street="123 Main St", city="Springfield")

    address = Address(street="123 Main St", city="Springfield", state="IL")
    assert address.street == helper.format_street("123 Main St")
    assert address.location == helper.format_location("Springfield", "IL", None)
    assert address.headers == config.HEADERS


@patch("whitepyges.helper.make_request_with_retries")
@patch("whitepyges.helper.get_endpoint")
def test_address_search(mock_get_endpoint, mock_make_request_with_retries):
    mock_get_endpoint.return_value = "http://mocked-url.com"
    mock_response = MagicMock()
    mock_response.text = """
    <div data-qa-selector="resident">
        <a class="tw-text-link tw-font-bold" href="/person/1">John Doe</a>
        <span class="tw-font-bold">30</span>
    </div>
    <div data-qa-selector="resident">
        <a class="tw-text-link tw-font-bold" href="/person/2">Jane Smith</a>
        <span class="tw-font-bold">--</span>
    </div>
    """
    mock_make_request_with_retries.return_value = mock_response

    address = Address(street="123 Main St", city="Springfield", state="IL")
    residents = address.search()

    assert len(residents) == 2
    assert residents[0] == {
        "name": "John Doe",
        "url": config.BASE_URL + "/person/1",
        "age": "30",
    }
    assert residents[1] == {
        "name": "Jane Smith",
        "url": config.BASE_URL + "/person/2",
        "age": None,
    }

    mock_get_endpoint.assert_called_once_with(
        "address", "address", address="123-Main-St", location=address.location
    )
    mock_make_request_with_retries.assert_called_once()


def test_address_repr_and_str():
    address = Address(street="123 Main St", city="Springfield", state="IL")
    with patch(
        "whitepyges.helper.format_repr", return_value="Mocked Repr"
    ) as mock_repr:
        assert repr(address) == "Mocked Repr"
        mock_repr.assert_called_once_with(address)

    with patch("whitepyges.helper.format_str", return_value="Mocked Str") as mock_str:
        assert str(address) == "Mocked Str"
        mock_str.assert_called_once_with(address)
