from five import grok
from ecreall.trashcan.interfaces import ITrashed, ITrashcanLayer
from plone.app.layout.viewlets.interfaces import IAboveContentBody
from OFS.interfaces import IFolder
from zope.app.publication.interfaces import IBeforeTraverseEvent
from zope.interface import alsoProvides


class ObjectTrashedViewlet(grok.Viewlet):
    grok.context(ITrashed)
    grok.viewletmanager(IAboveContentBody)


class YouAreInTheTrashcan(grok.Viewlet):
    grok.context(IFolder)
    grok.layer(ITrashcanLayer)
    grok.viewletmanager(IAboveContentBody)


@grok.subscribe(IFolder, IBeforeTraverseEvent)
def enterTrashcanMode(obj, event):
    try:
        if event.request.SESSION.get('trashcan', False):
            if not ITrashcanLayer.providedBy(event.request):
                alsoProvides(event.request, ITrashcanLayer)
    except AttributeError:
        # in test environment, we don't have SESSION
        pass
