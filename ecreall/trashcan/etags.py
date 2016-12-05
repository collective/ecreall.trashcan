from ecreall.trashcan.utils import get_session


class TrashcanEtag(object):
    """The ``trashcanetag`` etag component,
       returning if trashcan is open or closed
    """

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        session = get_session(getattr(self.published, 'context', self.published))
        trashcan = session and session.get('trashcan', False) or False
        return trashcan and '1' or '0'
