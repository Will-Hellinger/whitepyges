# Whitepyges

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

person = Person(first_name="John", last_name="Doe", state="WA")
results = person.search()

phone = Phone(number="123-456-7890")
carrier = phone.get_carrier()
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
