# Sheepped
[![Build Status](https://travis-ci.org/g4brielvs/sheepped.svg?branch=master)](https://travis-ci.org/sheepped/)
[![PyPI](https://img.shields.io/pypi/v/sheepped.svg)](https://pypi.python.org/pypi/sheepped)
[![Versions](https://img.shields.io/pypi/pyversions/sheepped.svg)](https://pypi.python.org/pypi/sheepped)

 🚚 A Python wrapper for tracking delivery (e.g. USPS).

* [Getting Started](#getting-started)
* [Usage](#usage)
* [Testing](#tests)
* [Versioning](#versioning)

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

## Versioning

Always suggest a version bump. We use [Semantic Versioning](http://semver.org).

    MICRO: the API is the same, no risk of breaking code
    MINOR: values have been added, existing values are unchanged
    MAJOR: existing values have been changed or removed