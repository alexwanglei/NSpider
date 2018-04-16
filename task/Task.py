

# class Task:
#     def __init__(self, id, type):
#         self.id = id
#         self.type = type


class FetchTask:
    def __init__(self, url, priority=0, repeat=0):
        self.url = url
        self.priority = priority
        self.repeat = repeat

    def __repr__(self):
        return "Task(%s, %s, %s)" % (self.url, self.priority, self.repeat)


class ParserTask:
    def __init__(self, raw, priority=0, repeat=0):
        self.raw = raw
        self.priority = priority
        self.repeat = repeat


class SaverTask():
    def __init__(self, result, priority=0, repeat=0):
        self.result = result
        self.priority = priority
        self.repeat = repeat