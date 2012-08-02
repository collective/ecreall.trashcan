## Script (Python) "canRestore"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan import ITrashedProvidedBy


if ITrashedProvidedBy(context):
    parent = context.getParentNode()
    if parent is not None and ITrashedProvidedBy(parent):
        return False
    return True
return False
