from zope.interface import alsoProvides
from zope.i18nmessageid import MessageFactory

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ecreall.trashcan.interfaces import ITrashcanLayer


PMF = MessageFactory('plone')

class ObjectTrashedViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlets_templates/objecttrashedviewlet.pt')


class YouAreInTheTrashcan(ViewletBase):
    index = ViewPageTemplateFile('viewlets_templates/youareinthetrashcan.pt')


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
        if not self.can_trash:
            return u""
        else:
            return self.index()

    def update(self):
        super(SwitchTrashcan, self).update()
        context = self.context
        mtool = getToolByName(context, 'portal_membership')
        if mtool.isAnonymousUser():
            self.can_trash = False
            return
        else:
            self.can_trash = context.unrestrictedTraverse('canTrash')() \
                or mtool.checkPermission('Add portal content', context)

        if self.context.unrestrictedTraverse('isTrashcanOpened')():
            self.title = PMF("Close trashcan")
            self.url = self.context.absolute_url() + '/closeTrashcan'
            self.icon = self.portal_url + '/ecreall-trashcan-open.png'
        else:
            self.title = PMF("Open trashcan")
            self.url = self.context.absolute_url() + '/openTrashcan'
            self.icon = self.portal_url + '/ecreall-trashcan.png'
