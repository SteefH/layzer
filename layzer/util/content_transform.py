from bs4 import BeautifulSoup

class Transformer(object):

    def __init__(self):
        pass

    def transform(self, content):
        doc = BeautifulSoup(content)
        doc = self._target_blank(doc)
        return self._get_content(doc)


    def _target_blank(self, doc):
        for a in doc.find_all('a'):
            a['target'] = '_blank'
        return doc

    def _get_content(self, doc):
        return unicode(doc)
