# Sheepped

 🚚 A Python wrapper for tracking delivery (e.g. USPS).

## Getting Started

First, install the package from [PyPI using `pip`](https://pypi.org/project/pip/).

    $ pip install sheepeed

Now, register at [USPS](https://registration.shippingapis.com) to get your `USPS_USER_ID`.

## Usage

Suppose you have set an environment variable `USPS_USER_ID` with your USPS ID and your tracking number is `42`:

```python
from sheepped import USPS


usps = USPS()
usps.track("42")
```

If you have a bucnh of tracking numbers, you might want to use the async API:

```python
import asyncio

from sheepped import USPS

usps = USPS()

async def main():
    tracking_numbers = ("1", "2", "3", "5", "8", "13", "21")
    tasks = tuple(usps.aiotrack(n) for n in tracking_numbers)
    return await asyncio.gather(*tasks)

asyncio.run(main())
```

## Tests

    $ python setup.py test