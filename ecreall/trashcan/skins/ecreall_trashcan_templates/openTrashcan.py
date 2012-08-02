## Script (Python) "openTrashcan"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

context.REQUEST.SESSION['trashcan'] = True
context.REQUEST.response.redirect(context.absolute_url())
