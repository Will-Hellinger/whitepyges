# Address


## Developer docs

::: whitepyges.address.Address

---

## Features

- Search for residents at a specific address
- Returns names, profile URLs, and ages (if available)
- Handles request retries and optional header randomization

---

## Example Usage

```python
from whitepyges import Address

address: Address = Address(street='123 Test Street', city='New York', state='NY')
info: dict = address.search()

print(info)
```

## Example Response

```json
--8<-- "docs/responses/address/search.json"
```