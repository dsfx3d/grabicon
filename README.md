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
# either
grabber = FaviconGrabber(url)
favicons = grabber.grab()
# or
another_grabber = FaviconGrabber()
favicons = another_grabber.grab(url)


favicons        # is a list of icons
icon = favicons[0]
type(icon)      # = <class 'Icon'>


# Icon is an entity class defined in grabicon
icon.url        # favicon url
icon.filetype   # filetypes [ raster-image, raw-image, vector-image, 3d-image]
icon.extension  # icon file extensions

icon.data       # bytes of image
icon.width      # width of image
icon.height     # height of image
```