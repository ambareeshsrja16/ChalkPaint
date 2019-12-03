from collections import namedtuple

class Chalk_Point:
    def __init__(self,
                 size_of_cache,
                 website_server,
                 caching_policy):
        """
        :param size_of_cache:
        :param website_server:
        :param caching_policy:
        """

        self.size_of_cache = size_of_cache
        self.website_server = website_server
        self.caching_policy = caching_policy

        self.main_cache = URL_Content_Hashmap(max_size=self.size_of_cache)

    def fetch_content(self, url_request):
        """

        :param url_request:
        :return:
        """

        #TODO
        assert isinstance(url_request, str)

        cache_check_inst =  self.check_in_cache(url_request)

        if cache_check_inst.found: # URL is found in cache, returning the content
            return cache_check_inst.content

        else:
            #TODO
            _content = self.request_server(url_request)

            cache_response = self.store_in_cache(url_request, _content)

            if cache_response:
                # TODO
                # Maybe note somewhere that this was successfully cached?
                # TODO IDEA
                # Use a secondary cache structure for objects/keys cached long ago? This should be slower than your current cache, but faster than reading directly from memory
                return _content
            else:
                #TODO
                #TODO Document how to deal with this!
                print("Not cached! Cache Error")

    def check_in_cache(self, url_request):
        """

        :param self:
        :param url_request:
        :return:
        """
        cache_check_inst = Cache_check()

        if url_request in self.main_cache.dictionary:
            cache_check_inst.found = True
            cache_check_inst.content = self.main_cache.dictionary[url_request]

        #TODO Add provision for secondary checks and other cache policies here


        return cache_check_inst


    def store_in_cache(self, url_request, content):
        """
        :param url_request:
        :param content:
        :return:
        """

        try:
            self.main_cache[url_request] = content
        except

    def request_server(self, url_request):
        """

        :param url_request:
        :return:
        """

class Cache_check:
    def __init__(self):
        self.found = False
        self.content = None


class URL_Content_Hashmap:
    def __init__(self, max_size):
        """

        :param size:
        """
        self.max_size = max_size
        self.dictionary = dict()

    def __len__(self):
        """Returns size of Hashmap"""
        return len(self.dictionary)

    def is_full(self):
        """
        Returns if the Hashmap has reached full capacity, specified under max_size instance variable

        :return: Bool
        """
        if len(self) >= self.max_size:
            return True
        else:
            return False









