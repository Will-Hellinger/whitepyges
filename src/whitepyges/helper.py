import random
import requests
import cloudscraper
import urllib.robotparser

from . import config


def format_name(first_name: str, last_name: str) -> str:
    """
    Format a first and last name into a single string

    Args:
        first_name (str): The first name of the person
        last_name (str): The last name of the person

    Returns:
        str: The formatted name
    """

    formatted_first_name: str = first_name.title().strip().replace(" ", "-")
    formatted_last_name: str = last_name.title().strip().replace(" ", "-")

    return f"{formatted_first_name}-{formatted_last_name}"


def validate_zip_code(zip_code: str | int) -> str:
    """
    Validate a zip code

    Args:
        zip_code (str | int): The zip code to validate

    Returns:
        str: The validated zip code
    """

    if zip_code is None:
        return ""

    formated_zip_code: str = str(zip_code).strip().replace(" ", "")

    if len(formated_zip_code) != 5:
        raise ValueError("Zip code must be 5 digits")

    return formated_zip_code


def format_location(city: str = None, state: str = None, zip_code: str = None) -> str:
    """
    Format a location into a single string

    Args:
        city (str): The city of the location
        state (str): The state of the location
        zip_code (str): The zip code of the location

    Returns:
        str: The formatted location

    Note:
        The zip code will take precedence over the city and state, then state, and finally zip code.
        If none of the values are provided, an empty string will be returned.
    """

    if (state and isinstance(state, str)) and len(state) != 2:
        raise ValueError("State must be a two-letter abbreviation")

    formatted_city = city.strip().replace(" ", "-").title() if city else None
    formatted_state = state.upper() if state else None

    if formatted_city and formatted_state:
        return f"{formatted_city}-{formatted_state}"

    elif formatted_state:
        return formatted_state

    elif zip_code:
        zip_code = validate_zip_code(zip_code)

        if len(zip_code) != 5:
            raise ValueError("Zip code must be 5 digits")

        return zip_code

    return ""


def format_age(age: int | None = None) -> str | None:
    """
    Format an age

    Args:
        age (int | None): The age to format

    Returns:
        str: The formatted age
    """

    if age is None:
        return None

    if age < 0:
        raise ValueError("Age must be a positive integer")

    return f"{int(age) // 10 * 10}s"


def format_street(street: str) -> str:
    """
    Format a street address

    Args:
        street (str): The street address to format

    Returns:
        str: The formatted street address

    Note:
        This only affects the spaces in the street address
    """

    return str(street).strip().replace(" ", "-")


def format_phone_number(phone_number: str) -> str:
    """
    Format a phone number

    Args:
        phone_number (str): The phone number to format

    Returns:
        str: The formatted phone number
    """

    allowed_characters: str = "0123456789-"

    replace_characters: dict = {
        "(": "",
        ")": "",
        ".": "",
        " ": "",
        "-": "",
    }

    country_code: str = "1"
    formatted_phone_number: str = phone_number.strip()

    # Replace invalid characters
    for char, replacement in replace_characters.items():
        formatted_phone_number = formatted_phone_number.replace(char, replacement)

    # Check for invalid characters
    for char in formatted_phone_number:
        if char not in allowed_characters:
            raise ValueError("Invalid phone number")

    if len(formatted_phone_number) == 11:
        country_code = formatted_phone_number[0]
        formatted_phone_number = formatted_phone_number[1:]

    if len(formatted_phone_number) == 10:
        formatted_phone_number = f"{country_code}-{formatted_phone_number[:3]}-{formatted_phone_number[3:6]}-{formatted_phone_number[6:]}"

    if not formatted_phone_number.startswith(f"{country_code}-"):
        formatted_phone_number = f"{country_code}-{formatted_phone_number}"

    if len(formatted_phone_number) != 14:
        raise ValueError("Invalid phone number")

    return formatted_phone_number


def get_endpoint(category: str, endpoint_type: str, **kwargs) -> str:
    """
    Retrieve the endpoint URL based on the category and endpoint type

    Args:
        category (str): The category of the endpoint (e.g., 'people', 'phone', 'address')
        endpoint_type (str): The type of endpoint (e.g., 'name', 'name_and_location')
        **kwargs: Additional arguments to format the endpoint URL

    Returns:
        str: The formatted endpoint URL
    """

    if config.ENDPOINTS.get(category) is None:
        raise ValueError(f"Category '{category}' not found in config")

    if config.ENDPOINTS[category].get(endpoint_type) is None:
        raise ValueError(
            f"Endpoint type '{endpoint_type}' not found in category '{category}'"
        )

    base_url: str = ""
    endpoint: str = config.ENDPOINTS[category][endpoint_type]

    if config.ENDPOINTS[category].get("use_base"):
        base_url = config.BASE_URL

    return f"{base_url}{endpoint.format(**kwargs)}"


def get_random_headers() -> dict:
    """
    Retrieve a random set of headers for the request

    Returns:
        dict: The headers for the request
    """

    return {
        "User-Agent": random.choice(config.USER_AGENTS),
        "Accept-Language": random.choice(config.ACCEPT_LANGUAGES),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
    }


def request_allowed_by_robots(
    url_to_check: str,
    user_agent: str = None,
    robots_url: str = "https://www.whitepages.com/robots.txt",
) -> bool:
    """
    Check if a request is allowed by the robots.txt file

    Args:
        url_to_check (str): The URL to check
        user_agent (str, optional): The user agent to check. Defaults to None.
        robots_url (str, optional): The URL of the robots.txt file. Defaults to "https://www.whitepages.com/robots.txt".

    Returns:
        bool: True if the request is allowed, False otherwise
    """

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    if user_agent is None:
        user_agent = config.HEADERS["User-Agent"]

    return rp.can_fetch(user_agent, url_to_check)


def make_request_with_retries(
    url: str,
    input_headers: dict,
    max_retries: int = 3,
    timeout: int = 10,
    ignore_robots: bool = False,
) -> requests.Response:
    """
    Make a request with retries using cloudscraper

    Args:
        url (str): The URL to request
        input_headers (dict): The headers to use for the request
        max_retries (int): The maximum number of retries
        timeout (int): The timeout for the request
        ignore_robots (bool): Ignore the robots.txt file

    Returns:
        requests.Response: The response from the request

    Note:
        This function will raise an exception if the request is not allowed by the robots.txt file
        (Unless the ignore_robots flag is set to True)
    """

    if not request_allowed_by_robots(url) and not ignore_robots:
        raise requests.exceptions.HTTPError(
            "Sorry! This request not allowed by robots.txt"
        )

    scraper: cloudscraper.CloudScraper = cloudscraper.create_scraper()

    for _ in range(max_retries):
        try:
            response: requests.Response = scraper.get(
                url, headers=input_headers, allow_redirects=True, timeout=timeout
            )
            response.raise_for_status()

            if "Just a moment..." in response.text:
                continue

            return response
        except requests.exceptions.HTTPError:
            continue

    raise requests.exceptions.HTTPError(
        f"Failed to retrieve a valid response after {max_retries} retries"
    )


def format_repr(obj: object) -> str:
    """
    Format the representation of an object

    Args:
        obj (object): The object to format

    Returns:
        str: The formatted representation of the object
    """

    class_name: str = obj.__class__.__name__
    attributes: dict = obj.__dict__

    formatted_attributes: str = ", ".join(
        [f"{key}='{value}'" for key, value in attributes.items()]
    )

    return f"{class_name}({formatted_attributes})"


def format_str(obj: object) -> str:
    """
    Format the representation of an object

    Args:
        obj (object): The object to format

    Returns:
        str: The formatted representation of the object
    """

    class_name: str = obj.__class__.__name__
    attributes: dict = obj.__dict__

    formatted_attributes: str = ", ".join(
        [f"{key}='{value}'" for key, value in attributes.items()]
    )

    return f"{class_name}({formatted_attributes})"
