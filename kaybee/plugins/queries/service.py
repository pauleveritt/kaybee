class Query:
    def __init__(self, docname):
        self.docname = docname

    @classmethod
    def filter(cls,
               collection):
        results = collection
        return results
