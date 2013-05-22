## Script (Python) "object_restore"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan import noLongerProvidesITrashed
from ecreall.trashcan import trashcanMessageFactory as _
from Products.CMFPlone.utils import safe_unicode

if not context.canTrash():
    raise Unauthorized


noLongerProvidesITrashed(context)
msg = _(u"'${title}' has been restored.",
        mapping={'title': safe_unicode(context.title_or_id())})

if context.REQUEST.get('ajax_load', False):
    return context.translate(msg)
else:
    context.plone_utils.addPortalMessage(msg)
    context.getParentNode().closeTrashcan()
