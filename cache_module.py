class Cache:
    def __init__(self,
                 size_of_cache=1000,
                 caching_policy="NON_LRU"):
        """
        :param size_of_cache:
        :param website_server:
        :param caching_policy:
        """
        self.size_of_cache = size_of_cache
        self.caching_policy = caching_policy
        self.main_cache = URL_Content_Hashmap(self.size_of_cache, self.caching_policy)  # TODO : Different one for LRU

    def __getitem__(self, item):
        return self.main_cache.__getitem__(item)

    def __setitem__(self, key, value):
        self.main_cache[key] = value


class URL_Content_Hashmap(dict):
    def __init__(self, max_size, cache_type="NON_LRU"):
        """
        :param size:
        """
        super().__init__()
        self.max_size = max_size
        self.cache_type = cache_type

    def is_full(self):
        """
        Returns if the Hashmap has reached full capacity, specified under max_size instance variable
        :return: Bool
        """
        if self.cache_type != "LRU":
            return True

        # LRU Cache, need to check size
        if len(self) >= self.max_size:
            return True
        else:
            return False


if __name__ == '__main__':
    print("Do testing")
    # Initialize test cases and run them here!
    # TODO







