## Script (Python) "canTrash"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

# Override this script for special use
return context.portal_membership.checkPermission('Delete objects', context)
