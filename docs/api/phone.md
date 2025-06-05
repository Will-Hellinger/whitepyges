# Phone

## Developer docs

::: whitepyges.phone.Phone

---

## Features

- Lookup phone numbers to retrieve spam risk, state, cities, area code, and profile URL
- Handles request retries and optional header randomization

---

## Example Usage

```python
from whitepyges import Phone

phone: Phone = Phone(phone_number='123-456-7890')
info: dict = phone.search()

print(info)
```

## Example Response

```json
--8<-- "docs/responses/phone/search.json"
```