from Acquisition import aq_get
from Products.PythonScripts.Utility import allow_module
allow_module('ecreall.trashcan.utils.get_session')

def get_session(obj):
    # Don't use request.SESSION because it uses
    # session_data_manager.getSessionData(create=1)
    # and so create a TransientObject for each webdav request (because it
    # doesn't use cookie) and you get finally a "MaxTransientObjectsExceeded:
    # 1000 exceeds maximum number of subobjects 1000"
    request = aq_get(obj, 'REQUEST', None)
    if request is None:
        # in test environment, we don't have REQUEST
        return

    session_data_manager = getattr(obj, 'session_data_manager', None)
    if session_data_manager is None:
        # in test environment, we don't have session_data_manager
        return

    session = session_data_manager.getSessionData(create=False)
    if session is None:
        return

    return session
