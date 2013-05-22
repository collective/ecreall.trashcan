## Script (Python) "object_trash"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan import providesITrashed
from ecreall.trashcan import trashcanMessageFactory as _
from AccessControl import Unauthorized
from Products.CMFPlone.utils import safe_unicode

if not context.canTrash():
    raise Unauthorized

providesITrashed(context)
msg = _(u"'${title}' has been moved to trashcan.",
        mapping={'title': safe_unicode(context.title_or_id())})

if context.REQUEST.get('ajax_load', False):
    return context.translate(msg)
else:
    context.plone_utils.addPortalMessage(msg)
    context.REQUEST.response.redirect(context.getParentNode().absolute_url())
