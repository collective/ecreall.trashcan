from OFS.interfaces import IFolder
from zope.app.publication.interfaces import IBeforeTraverseEvent
from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

from five import grok

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ecreall.trashcan.interfaces import ITrashed, ITrashcanLayer


PMF = MessageFactory('plone')

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


class SwitchTrashcan(ViewletBase):

    index = ViewPageTemplateFile('viewlets_templates/switchtrashcan.pt')

    def render(self):
        if not self.context.unrestrictedTraverse('canTrash')():
            return u""
        else:
            return self.index()

    def update(self):
        super(SwitchTrashcan, self).update()
        if self.context.unrestrictedTraverse('isTrashcanOpened')():
            self.title = PMF("Close trashcan")
            self.url = self.context.absolute_url() + '/closeTrashcan'
            self.icon = self.portal_url + '/ecreall-trashcan-open.png'
        else:
            self.title = PMF("Open trashcan")
            self.url = self.context.absolute_url() + '/openTrashcan'
            self.icon = self.portal_url + '/ecreall-trashcan.png'
