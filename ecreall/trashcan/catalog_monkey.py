from DateTime import DateTime
from Products.CMFCore.permissions import AccessInactivePortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.ZCatalog.ZCatalog import ZCatalog
from ecreall.trashcan.interfaces import ITrashed
from plone.indexer import indexer
from zope.interface import Interface


def searchResultsTrashed(self, REQUEST=None, **kw):
    kw = kw.copy()
    show_inactive = kw.get('show_inactive', False)

    user = _getAuthenticatedUser(self)
    kw['allowedRolesAndUsers'] = self._listAllowedRolesAndUsers(user)

    if (not show_inactive and
        not _checkPermission(AccessInactivePortalContent, self)):
        kw['effectiveRange'] = DateTime()

    request = getattr(self, 'REQUEST', None)
    if request is None:
        session = None
    else:
        session = getattr(self.REQUEST, 'SESSION', None)

    if 'trashed' not in kw:
        kw['trashed'] = session and session.get('trashcan', False) or False

    return ZCatalog.searchResults(self, REQUEST, **kw)


@indexer(Interface)
def trashed(obj):
    return ITrashed.providedBy(obj)
