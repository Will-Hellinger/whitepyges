import requests
from bs4 import BeautifulSoup

from . import helper
from . import config


class Phone:
    """
    A class to represent a phone number
    """

    def __init__(self, phone_number: str) -> None:
        """
        Initialize a new Phone object

        Args:
            phone_number (str): The phone number to search

        Returns:
            None
        """

        if not phone_number:
            raise ValueError("Phone number is required")

        self.phone_number = helper.format_phone_number(phone_number)

        self.headers = config.HEADERS

    def search(
        self,
        timeout: int = 10,
        max_retries: int = 3,
        randomize_headers: bool = False,
        ignore_robots: bool = False,
    ) -> dict | None:
        """
        Perform a search for the phone number

        Args:
            timeout (int, optional): The timeout for the request. Defaults to 10.
            max_retries (int, optional): The maximum number of retries. Defaults to 3.
            randomize_headers (bool, optional): Randomize the headers for the request. Defaults to False.
            ignore_robots (bool, optional): Ignore the robots.txt file. Defaults to False.

        Returns:
            list[dict] | None: Possible data for the phone number
        """

        endpoint: str = "number"

        url: str = helper.get_endpoint("phone", endpoint, number=self.phone_number)

        headers: dict = self.headers
        if randomize_headers:
            headers = helper.get_random_headers()

        response: requests.Response = helper.make_request_with_retries(
            url, headers, max_retries, timeout, ignore_robots
        )

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        phone_info_div = soup.find(
            "div", {"data-qa-selector": "phone-header-area-code-info"}
        )
        spam_info_div = soup.find("a", {"class": "wp-chip"})

        if not phone_info_div and not spam_info_div:
            return None

        splitting_info: tuple[str] = (
            "Area Code & Provider Details",
            "Area code location",
            "Other major (",
            ") cities",
        )

        phone_info: str = phone_info_div.get_text(strip=True)
        phone_info_list: list[str] = []

        for info in splitting_info:
            if info in phone_info:
                split_info: list[str] = phone_info.split(info, maxsplit=1)

                phone_info_list.append(split_info[0])
                phone_info = split_info[1]

        spam_info: str = "No spam info available"
        if spam_info_div:
            spam_info = spam_info_div.get_text(strip=True)

        formatted_phone_info: dict = {
            "spam_info": spam_info,
            "state": phone_info_list[2],
            "cities": phone_info_list[3],
            "area_code": phone_info_list[1],
            "url": url,
        }

        return formatted_phone_info

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
