import pytest

from whitepyges.helper import (
    format_name,
    validate_zip_code,
    format_location,
    format_age,
    format_street,
    format_phone_number,
)


def test_format_name():
    assert format_name("john", "doe") == "John-Doe"
    assert format_name("  john  ", "  doe  ") == "John-Doe"
    assert format_name("john paul", "doe") == "John-Paul-Doe"


def test_validate_zip_code():
    assert validate_zip_code(12345) == "12345"
    assert validate_zip_code(" 12345 ") == "12345"
    with pytest.raises(ValueError):
        validate_zip_code(1234)
    with pytest.raises(ValueError):
        validate_zip_code("123456")
    assert validate_zip_code(None) == ""


def test_format_location():
    assert format_location(city="New York", state="NY") == "New-York-NY"
    assert format_location(state="NY") == "NY"
    assert format_location(zip_code="12345") == "12345"
    assert (
        format_location(city="Los Angeles", state="CA", zip_code="12345")
        == "Los-Angeles-CA"
    )
    with pytest.raises(ValueError):
        format_location(state="California")


def test_format_age():
    assert format_age(25) == "20s"
    assert format_age(30) == "30s"
    assert format_age(None) is None
    with pytest.raises(ValueError):
        format_age(-5)


def test_format_street():
    assert format_street("123 Main St") == "123-Main-St"
    assert format_street("  456 Elm St  ") == "456-Elm-St"


def test_format_phone_number():
    assert format_phone_number("(123) 456-7890") == "1-123-456-7890"
    assert format_phone_number("123.456.7890") == "1-123-456-7890"
    assert format_phone_number("1234567890") == "1-123-456-7890"
    with pytest.raises(ValueError):
        format_phone_number("123-45-6789")
    with pytest.raises(ValueError):
        format_phone_number("invalid-phone")
