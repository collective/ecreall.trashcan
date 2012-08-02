## Script (Python) "isTrashcanOpened"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

session = getattr(context.REQUEST, 'SESSION', None)
return session and session.get('trashcan', False) or False
