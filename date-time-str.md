In Python, the `datetime` module provides classes for manipulating dates and times. To format date and time objects into strings and parse strings back into date and time objects, you can use the `strftime` (string format time) and `strptime` (string parse time) methods, respectively. These methods use format codes to specify the desired format.

Here's a quick reference for some common format codes:

- `%Y` : Year with century (e.g., `2024`)
- `%y` : Year without century, zero-padded (e.g., `24`)
- `%m` : Month as a zero-padded decimal number (e.g., `01` for January)
- `%d` : Day of the month as a zero-padded decimal number (e.g., `09`)
- `%H` : Hour (24-hour clock) as a zero-padded decimal number (e.g., `14` for 2 PM)
- `%I` : Hour (12-hour clock) as a zero-padded decimal number (e.g., `02` for 2 PM)
- `%p` : AM or PM (e.g., `PM`)
- `%M` : Minute as a zero-padded decimal number (e.g., `05`)
- `%S` : Second as a zero-padded decimal number (e.g., `09`)
- `%f` : Microsecond as a decimal number, zero-padded on the left (e.g., `000001`)
- `%z` : UTC offset in the form `+HHMM` or `-HHMM` (empty string if the object is naive)
- `%Z` : Time zone name (e.g., `UTC`, `EST`, empty string if the object is naive)
- `%A` : Full weekday name (e.g., `Wednesday`)
- `%a` : Abbreviated weekday name (e.g., `Wed`)
- `%B` : Full month name (e.g., `January`)
- `%b` : Abbreviated month name (e.g., `Jan`)
- `%c` : Locale’s appropriate date and time representation (e.g., `Tue Aug 16 21:30:00 1988`)
- `%x` : Locale’s appropriate date representation (e.g., `08/16/88`)
- `%X` : Locale’s appropriate time representation (e.g., `21:30:00`)

### Example Usage

#### Formatting a `datetime` object into a string

```python
from datetime import datetime

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_date)  # Output: 2024-05-30 14:35:22 (example)
```

#### Parsing a string into a `datetime` object

```python
from datetime import datetime

date_string = "2024-05-30 14:35:22"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(parsed_date)  # Output: 2024-05-30 14:35:22
```

### Custom Formatting Examples

#### Custom date format

```python
formatted_date = now.strftime("%A, %B %d, %Y")
print(formatted_date)  # Output: Thursday, May 30, 2024
```

#### Custom time format

```python
formatted_time = now.strftime("%I:%M %p")
print(formatted_time)  # Output: 02:35 PM
```

These examples demonstrate how you can control the format of date and time representations in your Python applications using the `strftime` and `strptime` methods.

---

To reverse the format from `%Y-%m-%d` (which represents `YYYY-MM-DD`) to `%d-%m-%Y` (which represents `DD-MM-YYYY`), you need to follow these steps:

1. Parse the original string into a `datetime` object using `strptime`.
2. Format the `datetime` object into the new desired string format using `strftime`.

Here's a complete example in Python:

```python
from datetime import datetime

# Original date string in YYYY-MM-DD format
original_date_string = "2024-05-30"

# Parse the original date string into a datetime object
date_object = datetime.strptime(original_date_string, "%Y-%m-%d")

# Format the datetime object into the new desired format (DD-MM-YYYY)
new_date_string = date_object.strftime("%d-%m-%Y")

print(new_date_string)  # Output: 30-05-2024
```

### Explanation:

1. **Parsing the String**: `datetime.strptime(original_date_string, "%Y-%m-%d")` converts the string `"2024-05-30"` into a `datetime` object.
2. **Formatting the Datetime Object**: `date_object.strftime("%d-%m-%Y")` converts the `datetime` object back into a string in the new format, resulting in `"30-05-2024"`.

This method can be adapted to reverse or change between any date formats as needed by adjusting the format strings in `strptime` and `strftime`.