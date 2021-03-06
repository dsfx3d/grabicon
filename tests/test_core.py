import io
import requests
from unittest import TestCase

from grabicon import FaviconGrabber, Icon
from .www import ServerRunner



class IconTestCase(TestCase):

    def test_method_create_returns_none_if_arg_data_is_not_image_data_buffer(self):
        data = io.BytesIO(b'16gh')
        icon = Icon.create('fb.io', data)

        self.assertIsNone(icon)


class FaviconGrabberTestCase(TestCase):


    def setUp(self):
        self.server = ServerRunner('t1', 'http-server', 1)
        self.server.start()

        self.index_url = 'http://127.0.0.1:80/'
        self.index_url_no_protocol = '127.0.0.1:80/'
        self.no_favicon_endpoint = 'no-favicon'
        self.rel_icon_endpoint = 'rel-icon'
        self.rel_shortcut_icon_endpoint = 'rel-shortcut-icon'
        self.rel_apple_icons = 'rel-apple-icons'
        self.favicons_not_accessible_endpoint = 'favicon-not-accessible'
        self.duplicate_icon_urls = 'duplicate-urls'

        self.default_favicon_url = f'{self.index_url}favicon.ico'
        self.default_apple_icon_url = f'{self.index_url}apple-touch-icon.png'
        self.default_apple_precomposed_icon_url = f'{self.index_url}apple-touch-icon-precomposed.png'

        self.favicon_1_url = f'{self.index_url}static/icon.ico'
        self.favicon_2_url = f'{self.index_url}static/icon1.ico'


    def tearDown(self):
        self.server.close()


    def grab_favicons(self, endpoint=''):
        grabber = FaviconGrabber()
        url = self.index_url+endpoint
        return grabber.grab(url)


    def contains_url(self, icons, url): # pragma: no cover
        for icon in icons:
            if icon.url == url:
                return True
        
        return False




    ## default favicon
    def test_method_grab_alwayas_return_icons_if_they_exist_in_root_dir(self):
        favicons = self.grab_favicons()

        self.assertEqual(len(favicons), 3) # including apple icons

        self.assertTrue(self.contains_url(favicons, self.default_favicon_url))
        self.assertTrue(self.contains_url(favicons, self.default_apple_icon_url))
        self.assertTrue(self.contains_url(favicons, self.default_apple_precomposed_icon_url))
    ##



    ## no favicon
    def test_method_grab_returns_empty_list_if_no_favicon_in_markup_or_dir(self):
        favicons = self.grab_favicons(self.no_favicon_endpoint)
        self.assertTrue(isinstance(favicons, list))
    
    def test_method_grab_returns_empty_list_if_icons_in_markup_are_not_accessible(self):
        favicons = self.grab_favicons(self.favicons_not_accessible_endpoint)
        self.assertTrue(isinstance(favicons, list))
    ##



    ## favicons from markup
    def check_markup_icons(self, url):
        favicons = self.grab_favicons(url)
        self.assertEqual(len(favicons), 2 + 1 + 2)      # including favicon.ico and apple icons
        self.assertTrue(self.contains_url(favicons, self.favicon_1_url))
        self.assertTrue(self.contains_url(favicons, self.favicon_2_url))

    def test_method_grab_returns_list_of_all_icon_urls_with_link_tag_rel_icon_in_markup(self):
        self.check_markup_icons(self.rel_icon_endpoint)

    def test_method_grab_returns_list_including_all_icon_urls_with_link_tag_rel_shortcut_icon_in_markup(self):
        self.check_markup_icons(self.rel_shortcut_icon_endpoint)

    def test_method_grab_returns_list_including_all_icon_urls_with_link_tag_rel_apple_touch_icon_and_apple_touch_icon_precomposed_in_markup(self):
        self.check_markup_icons(self.rel_apple_icons)
    ##



    ## duplicate urls
    def test_method_grab_returns_list_excluding_duplicate_urls(self):
        favicons = self.grab_favicons(self.duplicate_icon_urls)
        self.assertEqual(len(favicons), 1 + 1 + 2)      # including favicon.ico and apple icons
        self.assertTrue(self.contains_url(favicons, self.favicon_1_url))
    ##

    def test_method_grab_raises_value_error_if_arg_url_is_none(self):
        with self.assertRaises(ValueError):
            grabber = FaviconGrabber()
            grabber.grab(None)

    
    ## misc - test for issue #1
    def test_method_grab_returned_icons_have_no_none_attrs(self):
        favicons = self.grab_favicons(self.rel_icon_endpoint)

        for icon in favicons:
            self.assertIsNotNone(icon.type)
            self.assertNotEqual(icon.type, [])

            self.assertIsNotNone(icon.extension)
            self.assertNotEqual(icon.extension, [])

    ## misc
    def test_method_grab_can_accept_url_without_protocol_to_provide_expected_results(self):
        grabber = FaviconGrabber()
        favicons  = grabber.grab(self.index_url_no_protocol)

        self.assertEqual(len(favicons), 3) # including apple icons

        self.assertTrue(self.contains_url(favicons, self.default_favicon_url))
        self.assertTrue(self.contains_url(favicons, self.default_apple_icon_url))
        self.assertTrue(self.contains_url(favicons, self.default_apple_precomposed_icon_url))