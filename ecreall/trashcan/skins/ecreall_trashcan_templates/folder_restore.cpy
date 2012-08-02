## Controller Python Script "folder_restore"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Restore objects from the trashcan
##

from ecreall.trashcan import trashcanMessageFactory as _
from ecreall.trashcan import restoreObjectsFromTrashcanByPaths


req = context.REQUEST
paths = req.get('paths', [])

status = 'failure'
message = _(u'Please select one or more items to restore.')

success, failure = restoreObjectsFromTrashcanByPaths(context, paths,
                                                     REQUEST=req)

if success:
    status = 'success'
    message = _(u'Item(s) restored.')

if failure:
    message = _(u'${items} could not be restored.',
                mapping={u'items': ', '.join(failure.keys())})

context.plone_utils.addPortalMessage(message)
return state.set(status=status)
