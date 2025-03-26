import json
import logging
import requests
from bs4 import BeautifulSoup

from . import helper
from . import config


class Person:
    """
    A class to represent a person
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int | None = None,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
    ) -> None:
        """
        Initialize a new Person object

        Args:
            first_name (str): The first name of the person
            last_name (str): The last name of the person
            age (int, optional): The age of the person. Defaults to None.
            city (str, optional): The city of the person. Defaults to None.
            state (str, optional): The state of the person. Defaults to None.
            zip_code (str, optional): The zip code of the person. Defaults to None.

        Returns:
            None
        """

        if not first_name or not last_name:
            raise ValueError("First name and last name are required")

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            raise ValueError("First name and last name must be strings")

        self.name = helper.format_name(first_name, last_name)
        self.age = helper.format_age(age)
        self.location = helper.format_location(city, state, zip_code)

        self.headers = config.HEADERS

        self.logger = logging.getLogger(f"Person-{self.name}")
        logging.basicConfig(level=logging.WARNING)

        self.logger.info(f"Initialized Person object: {repr(self)}")

    def _clean_person_data(self, person_data: dict, age: str) -> list[dict]:
        """
        Clean the person data by filtering and repositioning the items.

        Args:
            person_data (dict): The raw person data.
            age (str): The age of the person.

        Returns:
            list[dict]: The cleaned list of items.
        """

        raw_items: list[dict] = person_data.get("itemListElement", [])
        cleaned_items: list[dict] = []

        for item in raw_items:
            if item.get("@type") != "ListItem":
                continue

            item_data: dict = item.get("item", {})

            if item_data.get("@type") != "Person":
                continue

            if age is not None:
                if not item_data.get("description", "").startswith(
                    f"{item_data.get('name')} in their {age}"
                ) and not item_data.get("description", "").startswith(
                    f"{item_data.get('name')},"
                ):
                    continue

            cleaned_items.append(item)

        return cleaned_items

    def _reposition_element_list(self, element_list: list[dict]) -> list[dict]:
        """
        Reposition the elements in the list

        Args:
            element_list (list[dict]): The list of elements to reposition

        Returns:
            list[dict]: The repositioned list of elements
        """

        for i in range(0, len(element_list)):
            original_position: int = element_list[i].pop("position", 0)

            element_list[i]["currentPosition"] = i + 1
            element_list[i]["originalPosition"] = original_position

        return element_list

    def search(
        self,
        count: int = -1,
        timeout: int = 10,
        max_retries: int = 3,
        randomize_headers: bool = False,
        ignore_robots: bool = False,
    ) -> list[dict] | None:
        """
        Perform a search for the person

        Args:
            count (int, optional): The number of results to return. -1 returns all results. Defaults to -1.
            timeout (int, optional): The timeout for the request. Defaults to 10.
            max_retries (int, optional): The maximum number of retries. Defaults to 3.
            randomize_headers (bool, optional): Randomize the headers for the request. Defaults to False.
            ignore_robots (bool, optional): Ignore the robots.txt file. Defaults to False.

        Returns:
            list[dict] | None: Possible data for the person
        """

        if count == 0 or count < -1:
            self.logger.error("Count must be a positive integer or -1")
            raise ValueError("Count must be a positive integer or -1")

        endpoint: str = "name"

        if self.location:
            endpoint = "name_and_location"

        url: str = helper.get_endpoint(
            "people", endpoint, name=self.name, location=self.location
        )

        search_headers: dict = self.headers.copy()  # dont modify the original headers
        if randomize_headers:
            search_headers = helper.get_random_headers()

        response: requests.Response = helper.make_request_with_retries(
            url, search_headers, max_retries, timeout, ignore_robots
        )

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", type="application/ld+json")

        if not script_tag:
            self.logger.warning("No script tag found in the response")
            return None

        # This is only really a list with one item (I would assume this is for the pages of users)
        person_data: dict = json.loads(script_tag.string)[0]

        cleaned_items: list[dict] = self._clean_person_data(person_data, self.age)
        cleaned_items = self._reposition_element_list(cleaned_items)

        return cleaned_items[:count] if count != -1 else cleaned_items

    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the Person object.

        Returns:
            str: The unambiguous string representation of the Person object
        """

        return helper.format_repr(self)

    def __str__(self) -> str:
        """
        Return a readable string representation of the Person object.

        Returns:
            str: The readable string representation of the Person object
        """

        return helper.format_str(self)
