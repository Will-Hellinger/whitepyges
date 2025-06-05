# Usage

## Respecting robots.txt

Whitepyges retrieves information from Whitepages.com using web scraping techniques. By default, the library checks and abides by the site's `robots.txt` rules to ensure responsible and ethical scraping. This means that if a particular action is disallowed by `robots.txt`, Whitepyges will not perform that request.

### Overriding robots.txt

If you encounter issues where a search is blocked due to `robots.txt` restrictions, you can override this behavior by setting the `ignore_robots` parameter to `True` in your search methods. This will instruct Whitepyges to ignore the `robots.txt` rules and proceed with the request.

**Example:**

```python
from whitepyges import Address

address = Address(street="123 Main St", city="Springfield", state="IL")
# This will ignore robots.txt and perform the search anyway
residents = address.search(ignore_robots=True)
```

### Note

By default, Whitepyges respects robots.txt to comply with website policies. Use the ignore_robots option responsibly and only if you understand the implications of bypassing these restrictions.