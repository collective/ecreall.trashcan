from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from ecreall.trashcan.interfaces import IObjectTrashedEvent,\
    IObjectRestoredEvent


class ObjectTrashedEvent(ObjectEvent):
    implements(IObjectTrashedEvent)


class ObjectRestoredEvent(ObjectEvent):
    implements(IObjectRestoredEvent)