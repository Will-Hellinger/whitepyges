import requests
from bs4 import BeautifulSoup

from . import helper
from . import config


class Address:
    """
    A class to represent an address
    """

    def __init__(
        self,
        street: str = None,
        city: str = None,
        state: str = None,
        zip_code: str = None,
    ) -> None:
        """
        Initialize a new Address object

        Args:
            street (str): The street of the address
            city (str): The city of the address
            state (str): The state of the address
            zip_code (str): The zip code of the address

        Returns:
            None
        """

        if not street:
            raise ValueError("Street is required")

        if not city:
            raise ValueError("City is required")

        if not state and not zip_code:
            raise ValueError("State or zip code is required")

        self.street = helper.format_street(street)
        self.location = helper.format_location(city, state, zip_code)

        self.headers = config.HEADERS

    def search(
        self,
        timeout: int = 10,
        max_retries: int = 3,
        randomize_headers: bool = False,
        ignore_robots: bool = False,
    ) -> list[dict] | None:
        """
        Perform a search for the address

        Args:
            timeout (int, optional): The timeout for the request. Defaults to 10.
            max_retries (int, optional): The maximum number of retries. Defaults to 3.
            randomize_headers (bool, optional): Randomize the headers for the request. Defaults to False.
            ignore_robots (bool, optional): Ignore the robots.txt file. Defaults to False.

        Returns:
            list[dict] | None: Possible data for the address
        """

        endpoint: str = "address"

        url: str = helper.get_endpoint(
            "address", endpoint, address=self.street, location=self.location
        )

        headers: dict = self.headers
        if randomize_headers:
            headers = helper.get_random_headers()

        response: requests.Response = helper.make_request_with_retries(
            url, headers, max_retries, timeout, ignore_robots
        )

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        residents: list[dict] = []

        for div in soup.find_all("div", {"data-qa-selector": "resident"}):
            person_name: str = div.find(
                "a", class_="tw-text-link tw-font-bold"
            ).get_text(strip=True)
            person_url: str = div.find("a", class_="tw-text-link tw-font-bold")["href"]
            person_age: str = div.find("span", class_="tw-font-bold").get_text(
                strip=True
            )

            if person_age == "--":
                person_age = None

            person_data: dict = {
                "name": person_name,
                "url": config.BASE_URL + person_url,
                "age": person_age,
            }

            residents.append(person_data)

        return residents

    def __repr__(self) -> str:
        """
        Return the string representation of the object

        Returns:
            str: The string representation of the object
        """

        return helper.format_repr(self)

    def __str__(self) -> str:
        """
        Return the string representation of the object

        Returns:
            str: The string representation of the object
        """

        return helper.format_str(self)
