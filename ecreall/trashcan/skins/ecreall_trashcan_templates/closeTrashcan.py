## Script (Python) "openTrashcan"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan import ITrashedProvidedBy


context.REQUEST.SESSION['trashcan'] = False

obj = context
while ITrashedProvidedBy(obj):
    obj = obj.getParentNode()
context.REQUEST.response.redirect(obj.absolute_url() + '/view')
