.. contents::

This is an implementation of a trashcan for Plone.
This product monkey patch PloneCatalog.searchResults and PloneCatalog.__call__.
Since version 1.2, this product works only on Plone >= 3.3 (included Plone 4.x).

This product adds a "move to trashcan"/"restore" actions and
a "open trashcan"/"close trashcan" links at the bottom of the page.

When you move an object to the trashcan, the object is actually not moved anywhere.
It is just hidden from the search.
What the action does is setting a marker interface ITrashed on the object
and on sub-objects if the object trashed is a folder. It excludes the object
from navigation too.

To see the trashed objects, you have to activate the trashcan mode with
the "open trashcan" link at the bottom of your page.
You can see it as a parallel world. You will see only trashed objects and the search
now search only on trashed content.

In this mode you can restore objects. You can't restore object if the parent is trashed.
In this case you have to cut and paste the object in a non trashed folder to restore it.

When you are in trashcan mode, there is some verifications which takes place.
You can't paste an object in a trashed folder for example.

To come back to the normal mode, click on the "close trashcan" link at the bottom of the page.
When trahscan mode is closed, it returns to the nearest parent not trashed.

Code repository: https://svn.ecreall.com/public/ecreall.trashcan/

Integration with CacheFu
------------------------

In the plone-containers rule, edit "ETag Expression", replace::

  python:request.get('__cp',None) is not None

by::

  python:str(request.get('__cp',None) is not None) +'|'+ str(request.SESSION.get('trashcan', None))

Integration with plone.app.caching
----------------------------------

If you have a cache on folder views with plone.app.caching,
add 'trashed' to your etags.
