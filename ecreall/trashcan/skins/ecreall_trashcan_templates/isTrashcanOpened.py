## Script (Python) "isTrashcanOpened"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

from ecreall.trashcan.utils import get_session
session = get_session(context)
return session and session.get('trashcan', False) or False
