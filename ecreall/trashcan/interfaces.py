from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ITrashed(Interface):
    pass


class ITrashcanLayer(IDefaultBrowserLayer):
    pass
