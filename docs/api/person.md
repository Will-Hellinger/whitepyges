# Person

## Developer docs

::: whitepyges.person.Person

---

## Features

- Search for people by first name, last name, and state
- Returns names, profile URLs, addresses, phone numbers, and related people
- Handles request retries and optional header randomization

---

## Example Usage

```python
from whitepyges import Person

person: Person = Person(first_name='John', last_name='Doe', state='WA')
info: dict = person.search()

print(info)
```

## Example Response

```json
--8<-- "docs/responses/person/search.json"
```