# Sheepped

 🚚 A Python wrapper for tracking delivery (e.g. USPS).

## Getting Started

First, install the package from [pip](https://pypi.org/project/pip/).

    $ pip install sheepeed

Now, register at [USPS](https://registration.shippingapis.com) to get your ```USPS_USER_ID```.

## Usage

    $ from sheppeed import USPS
    $ usps = USPS('${USPS_USER_ID}')
    $ usps.track('${USPS_TRACKING_NUMBER}')