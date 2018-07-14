

# class Task:
#     def __init__(self, id, type):
#         self.id = id
#         self.type = type


class FetchTask:
    def __init__(self, url_id, url, type, priority=0, repeat=0):
        self.url_id = url_id
        self.url = url
        self.type = type
        self.priority = priority
        self.repeat = repeat

    def __repr__(self):
        return "%s(%s, %s, %s)" % (FetchTask.__name__, self.url, self.priority, self.repeat)

    def __str__(self):
        return self.__repr__()


class ParserTask:
    def __init__(self, url_id, raw, priority=0, repeat=0):
        self.url_id = url_id
        self.raw = raw
        self.priority = priority
        self.repeat = repeat

    def __repr__(self):
        return "%s(%s, %s, %s)" % (ParserTask.__name__, self.raw, self.priority, self.repeat)

    def __str__(self):
        return self.__repr__()


class SaverTask():
    def __init__(self, results, priority=0, repeat=0):
        self.results = results
        self.priority = priority
        self.repeat = repeat

    def __repr__(self):
        return "%s(%s, %s, %s)" % (SaverTask.__name__, self.results, self.priority, self.repeat)

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    print(FetchTask.__name__)