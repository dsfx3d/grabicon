import os
import io
from urllib.parse import urlparse

# dependencies
import requests
import fleep
from bs4 import BeautifulSoup




class Icon:
    '''
    entity class for FaviconGrabber

    url         - url of favicon
    data        - icon data
    size        - length of data in bytes
    type        - icon image type
    extension   - icon file extension
    '''
    @staticmethod
    def create(url, data):
        '''
        create and return valid Icon objects

        Accepts
        -------
        url     - url
        data    - data recieved from url

        Returns
        -------
        Icon    - if data is image
        None    - if data is not image
        '''
        icon = Icon()
        
        icon.url = url
        icon.data = data.read()

        # seek size of data
        data.seek(0, os.SEEK_END)
        icon.size = data.tell()

        #
        info = fleep.get(icon.data)
        icon.type = info.type[0] if len(info.type) > 0 else None
        icon.extension = info.extension[0] if len(info.extension) > 0 else None

        # if icon is not image return None
        if icon.type is None or 'image' not in icon.type:
            return None
        
        return icon

    def __str__(self):      # pragma: no cover
        return f'{self.size} - {self.type} - {self.extension} - {self.url}'




class FaviconGrabber:
    
    def __init__(self):
        '''
        raw_url:        requested url
        resolved_url:   url after resolving redirects of raw_url
        soup:           parsable response of resolved_url
        
        icons:          favicon dict, keys: url, width, height

        has_grabbed:        flag to check if favicons are grabbed
        '''
        pass




    def __init(self, url=None):
        '''
        initialize class variables

        Accepts
        -------
        url - requested url
        '''
        self.__raw_url = url
        self.__resolved_url = None
        self.__soup = None

        self.__icons = []

        self.__has_grabbed = False

        # clean and resolve raw_url redirects
        self.__resolve_raw_url()





    def __resolve_raw_url(self):
        '''
        clean raw_url and resolve redirects
        '''  
        url = self.__raw_url

        # add protocol to raw url if missing
        if not url.startswith('http'):
            url = 'http://'+url

        # go through redirects
        response = requests.get(url)
        # set final url as resolved_url
        self.__resolved_url = response.url
        # prepare soup
        self.__soup = BeautifulSoup(response.text, features='html.parser')





    def __get_absolute_url(self, url):
        '''
        get absolute url if url in args is relational

        Accepts
        -------
        url

        Returns
        -------
        url - if url is not absolute adds host and protocol
        '''
        # create url parsables
        favicon_url_parse = urlparse(url)
        # create resolved_url parsable
        resolved_url_parsable = urlparse(self.__resolved_url)

        # is icon url missing host domain
        if favicon_url_parse.netloc == '':
            # add resolved url's host domain
            favicon_url_parse = favicon_url_parse._replace(netloc=resolved_url_parsable.netloc)

        # is icon url missing protocol
        if favicon_url_parse.scheme == '':
            # add resolved url's protocol
            favicon_url_parse = favicon_url_parse._replace(scheme=resolved_url_parsable.scheme)
        
        return favicon_url_parse.geturl()





    def __extract_url_from_tag(self, tag):
        '''
        extract icon url from link tag

        Accepts
        -------
        tag - beautifulsoup link tag

        Returns
        -------
        absolute url extracted from link tag
        '''
        # extract icon url from attrs
        url = tag.get('href')
        
        # clean url
        url = self.__get_absolute_url(url)

        # return url
        return url





    def __extract_favicon_urls_from_html(self):
        '''
        extract favicon urls from html

        Returns
        -------
        set of icon urls scraped from requested page
        '''
        # scrape icon tags from soup
        icon_tags = set()
        rels = ['shortcut icon', 'icon', 'apple-touch-icon', 'apple-touch-icon-precomposed', 'SHORTCUT ICON', 'ICON', 'APPLE-TOUCH-ICON', 'APPLE-TOUCH-ICON-PRECOMPOSED']
        for rel in rels:
            tag = self.__soup.findAll('link', attrs={'rel': rel})
            icon_tags.update(tag)
        
        # extract icon urls from tags
        icon_urls = {self.__extract_url_from_tag(icon) for icon in icon_tags}

        return icon_urls





    def __get_alt_favicon_url(self):
        '''
        Returns
        -------
        default favicon url for requested page
        '''        
        url = self.__get_absolute_url('/favicon.ico')
        return url




    def __get_apple_touch_icon_url(self):
        '''
        Returns
        -------
        default apple touch icon url for requested page
        '''
        url = self.__get_absolute_url('/apple-touch-icon.png')
        return url




    def __get_apple_touch_icon_precomposed_url(self):
        '''
        Returns
        -------
        default apple touch precomposed icon url for requested page
        '''
        url = self.__get_absolute_url('/apple-touch-icon-precomposed.png')
        return url




    def __get_apple_icon_urls(self):
        '''
        Returns
        -------
        set of default apple touch icon urls
        '''
        apple_icon_urls = set()
        apple_icon_urls.add(self.__get_apple_touch_icon_url())
        apple_icon_urls.add(self.__get_apple_touch_icon_precomposed_url())

        return apple_icon_urls





    def __grab_favicon_urls(self):
        '''
        grab and return list of favicon urls
        
        Returns
        -------
        list of favicon urls extracted from
        '''
        # get icons from markup
        markup_icon_urls = self.__extract_favicon_urls_from_html()
        # get default favicon
        default_icon_url = self.__get_alt_favicon_url()
        # get apple icons
        apple_icon_urls = self.__get_apple_icon_urls()
        
        # enlist all favicon urls
        icon_urls = set()
        icon_urls.add(default_icon_url)
        icon_urls.update(markup_icon_urls)
        icon_urls.update(apple_icon_urls)
        
        # remove duplicate urls
        icon_urls = list(icon_urls)

        return icon_urls





    def __get_icon_from_url(self, url):
        '''
        fetches icon by passed url and returns Icon obj

        Accepts
        -------
        url - icon url

        Returns
        -------
        Icon object    - if valid icon fetched
        None           - if not valid icon not fetched
        '''
        # request url
        response = requests.get(url)
        
        # create and return Icon
        url = response.url
        data_buffer = io.BytesIO(response.content)

        return Icon.create(url, data_buffer)






    def __get_favicons(self, urls):
        '''
        get list of favicons from list of urls

        Accepts
        -------
        urls    - list of favicon urls
        
        Returns
        -------
        icons   - list of Icon(s)
        '''
        icons = []
        
        for url in urls:
            favicon = self.__get_icon_from_url(url)

            if favicon is not None:
                icons.append(favicon)
        
        return icons





    def grab(self, url):
        '''
        grab favicons

        Accepts
        -------
        url     - a valid url

        Returns
        -------
        icons   - list of core.Icon(s) attached with the requested url
        '''
        if url is None:
            raise ValueError('arg `url` is None')

        self.__init(url)
        
        # grab urls
        icon_urls = self.__grab_favicon_urls()

        # clean urls and return list of icons
        self.__icons = self.__get_favicons(icon_urls)

        # mark has_grabbed flag
        self.__has_grabbed = True

        return self.__icons