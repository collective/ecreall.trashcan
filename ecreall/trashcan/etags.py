from five import grok
from zope.interface import Interface
try:
    from plone.app.caching.interfaces import IETagValue
    HAS_PLONEAPPCACHING = True
except ImportError:
    HAS_PLONEAPPCACHING = False

if HAS_PLONEAPPCACHING:

    class TrashcanEtag(grok.MultiAdapter):
        """The ``trashcanetag`` etag component,
           returning if trashcan is open or closed
        """
        grok.name('trashed')
        grok.implements(IETagValue)
        grok.adapts(Interface, Interface)

        def __init__(self, published, request):
            self.published = published
            self.request = request

        def __call__(self):
            session = getattr(self.request, 'SESSION', None)
            trashcan = session and session.get('trashcan', False) or False
            return trashcan and '1' or '0'
