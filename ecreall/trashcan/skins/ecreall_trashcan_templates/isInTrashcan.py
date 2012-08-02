## Script (Python) "isInTrashcan"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan import ITrashedProvidedBy


return ITrashedProvidedBy(context)
