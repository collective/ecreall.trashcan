"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
from ecreall.trashcan.events import ObjectTrashedEvent, ObjectRestoredEvent
from zope.event import notify
trashcanMessageFactory = MessageFactory('ecreall.trashcan')

from Products.PythonScripts.Utility import allow_module
allow_module('ecreall.trashcan.ITrashedProvidedBy')
allow_module('ecreall.trashcan.providesITrashed')
allow_module('ecreall.trashcan.noLongerProvidesITrashed')
allow_module('ecreall.trashcan.moveObjectsToTrashcanByPaths')
allow_module('ecreall.trashcan.restoreObjectsFromTrashcanByPaths')
allow_module('ecreall.trashcan.api.trash')
allow_module('ecreall.trashcan.api.restore')
allow_module('ecreall.trashcan.api.is_trashed')

import transaction
from zope.interface import alsoProvides, noLongerProvides
from zope.annotation.interfaces import IAnnotations
from OFS.interfaces import IFolder
from AccessControl import Unauthorized
from AccessControl.requestmethod import postonly
from ZODB.POSException import ConflictError

from Products.CMFPlone.utils import transaction_note
from Products.CMFCore.utils import getToolByName

try:
    from Products.PluginIndexes.BooleanIndex.BooleanIndex import BooleanIndex
    HAS_BOOLEANINDEX = True
except ImportError:
    HAS_BOOLEANINDEX = False

from ecreall.trashcan.interfaces import ITrashed

KEY = 'ecreall.trashcan'


def ITrashedProvidedBy(context):
    return ITrashed.providedBy(context)


def providesITrashed(context):
    annotations = IAnnotations(context)
    infos = annotations.get(KEY, {'count': 0})
    infos['count'] += 1
    infos['ExcludeFromNav'] = context.getExcludeFromNav()
    annotations[KEY] = infos

    alsoProvides(context, ITrashed)
    context.setExcludeFromNav(True)
    notify(ObjectTrashedEvent(context))
    context.reindexObject(idxs=['trashed', 'object_provides'])

    if IFolder.providedBy(context):
        for obj in context.objectValues():
            providesITrashed(obj)


def noLongerProvidesITrashed(context):
    annotations = IAnnotations(context)
    infos = annotations.get(KEY, {'count': 0})
    infos['count'] -= 1
    annotations[KEY] = infos
    if infos['count'] <= 0:
        noLongerProvides(context, ITrashed)
        context.setExcludeFromNav(infos.get('ExcludeFromNav', False))
        context.reindexObject(idxs=['trashed', 'object_provides'])
        notify(ObjectRestoredEvent(context))

    if IFolder.providedBy(context):
        for obj in context.objectValues():
            noLongerProvidesITrashed(obj)


def pasteObject(obj, event):
    if event.newParent is None:
        # RemovedObjectEvent
        return

    if ITrashed.providedBy(event.newParent):
        raise Unauthorized("You can't paste into a trashcan")

    if ITrashed.providedBy(obj):
        annotations = IAnnotations(obj)
        annotations[KEY] = {'count': 0}
        noLongerProvides(obj, ITrashed)
        obj.reindexObject(idxs=['trashed', 'object_provides'])


# Copied from PloneTool.py:deleteObjectsByPaths and adapted to move to trashcan
def moveObjectsToTrashcanByPaths(self, paths, handle_errors=True,
                                 REQUEST=None):
    failure = {}
    success = []
    # use the portal for traversal in case we have relative paths
    portal = getToolByName(self, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        # Skip and note any errors
        if handle_errors:
            sp = transaction.savepoint(optimistic=True)

        try:
            obj = traverse(path)
            providesITrashed(obj)
            success.append('%s (%s)' % (obj.title_or_id(), path))
        except ConflictError:
            raise
        except Exception, e:
            if handle_errors:
                sp.rollback()
                failure[path] = e
            else:
                raise

    transaction_note('Moved to trashcan %s' % (', '.join(success)))
    return success, failure

moveObjectsToTrashcanByPaths = postonly(moveObjectsToTrashcanByPaths)


def restoreObjectsFromTrashcanByPaths(self, paths, handle_errors=True,
                                      REQUEST=None):
    failure = {}
    success = []
    # use the portal for traversal in case we have relative paths
    portal = getToolByName(self, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        # Skip and note any errors
        if handle_errors:
            sp = transaction.savepoint(optimistic=True)

        try:
            obj = traverse(path)
            if obj.canRestore():
                noLongerProvidesITrashed(obj)
                success.append('%s (%s)' % (obj.title_or_id(), path))
        except ConflictError:
            raise
        except Exception, e:
            if handle_errors:
                sp.rollback()
                failure[path] = e
            else:
                raise

    transaction_note('Restored %s' % (', '.join(success)))
    return success, failure

restoreObjectsFromTrashcanByPaths = postonly(restoreObjectsFromTrashcanByPaths)
