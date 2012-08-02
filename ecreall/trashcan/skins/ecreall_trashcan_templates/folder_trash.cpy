## Controller Python Script "folder_trash"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Move to trashcan objects from a folder
##

from ecreall.trashcan import trashcanMessageFactory as _
from ecreall.trashcan import moveObjectsToTrashcanByPaths


req = context.REQUEST
paths = req.get('paths', [])

status = 'failure'
message = _(u'Please select one or more items to move to trashcan.')

success, failure = moveObjectsToTrashcanByPaths(context, paths, REQUEST=req)

if success:
    status = 'success'
    message = _(u'Item(s) moved to trashcan.')

if failure:
    message = _(u'${items} could not be moved to trashcan.',
                mapping={u'items': ', '.join(failure.keys())})

context.plone_utils.addPortalMessage(message)
return state.set(status=status)
