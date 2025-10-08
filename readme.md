# Whitepyges

![image](./docs/images/logo.png)

[![Art by @stawbeby](https://img.shields.io/badge/Art%20by-%40stawbeby-green?style=for-the-badge&logo=instagram)](https://www.instagram.com/stawbeby/profilecard)


Whitepyges is an unoficial Python client library for retrieving public information from Whitepages.com

## ⚠️ Legal Disclaimer ⚠️

This software is provided for personal and educational use only. You are responsible for ensuring your use of this software complies with all applicable laws and third-party Terms of Service. Authors/Contributors do not condone or support the violation of any website's terms. Use at your own risk.

## What works

- Person lookup by name and location
- Phone number lookup by number alone
- Address information

## What doesnt work

- Carrier information for phones

## Installation

To install Whitepyges, use pip:

```bash
pip install whitepyges
```

locally:
```bash
git clone https://github.com/will-hellinger/whitepyges.git
cd whitepyges
pip install .
```

## Usage

Here is a basic example of how to use Whitepyges:

```python
import whitepyges

person: whitepyges.Person = whitepyges.Person(first_name='John', last_name='Doe', state="WA")
phone: whitepyges.Phone = whitepyges.Phone(phone_number='123-456-7890')
address: whitepyges.Address = whitepyges.Address(street='123 Test Street', city='New York', state='NY')

person_info = person.search()
phone_info = phone.search()
address_info = address.search()
```

## Responses

Note: All example responses have their info changed

Person:
```json
[
    {
        "name": "Jon Doe",
        "givenName": "Jon",
        "familyName": "Doe",
        "description": "Jon Doe in their 70s, currently living in Example, WA",
        "url": "https://www.whitepages.com/name/Jon-Doe/Example-WA/random_letters",
        "address": [
            {
                "@type": "PostalAddress",
                "streetAddress": "123 St",
                "addressLocality": "Example",
                "addressRegion": "WA",
                "addressCountry": "US"
            }
        ],
        "telephone": "(123) 456-7890",
        "relatedTo": []
    },
    {
        "name": "Jon Doe",
        "givenName": "Jon",
        "familyName": "Doe",
        "description": "Jon Doe in their 40s, currently living in Example-2, WA",
        "url": "https://www.whitepages.com/name/Jon-Doe/Example-2-WA/random_letters2",
        "address": [
            {
                "@type": "PostalAddress",
                "streetAddress": "123 Ave",
                "addressLocality": "Example-2",
                "addressRegion": "WA",
                "addressCountry": "US"
            }
        ],
        "telephone": "(123) 456-7890",
        "relatedTo": []
    }
]
```

Phone:
```json
{
    "spam_info": "LOW SPAM RISK",
    "state": "Washington",
    "cities": "Example, Example-2, Examples 3",
    "area_code": "123",
    "url": "https://www.whitepages.com/phone/1-123-456-7890"
}
```

Address:
```json
[
    {
        "name": "Jon Doe",
        "url": "https://www.whitepages.com/name/Jon-Doe/Example-WA/random_numbers",
        "age": "22"
    },
    {
        "name": "Jon Doe-2",
        "url": "https://www.whitepages.com/name/Jon-Doe-2/Example-WA/random_numbers-2",
        "age": null
    }
]
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## Formatting

When contributing, please follow these formatting guidelines:

- Format your code with [Black](https://black.readthedocs.io/en/stable/).
- Ensure all public methods and classes have docstrings.
- Write unit tests for new features and bug fixes.
- Use meaningful commit messages.

By adhering to these guidelines, you help maintain the readability and quality of the codebase.

## Contact

For any questions or suggestions, please open an issue on GitHub.
