# Favicon Grabber

grab all favicons attached to a webpage

## Installation

`pip install grabicon`

## Usage

```python
from grabicon import FaviconGrabber
```

## Example

```python
# grab favicons using
grabber = FaviconGrabber()
favicons = grabber.grab(url)

# grab more favicons
more_favicons = grabber.grab(other_url)


favicons        # is a list of icons
icon = favicons[0]
type(icon)      # = <class 'grabicon.core.Icon'>


# Icon is an entity class defined in grabicon
icon.url        # favicon url
icon.data       # bytes of image
icon.size       # size of data in bytes
icon.type       # file types [ raster-image, raw-image, vector-image, 3d-image]
icon.extension  # icon file extensions
```