from ecreall.trashcan import providesITrashed, noLongerProvidesITrashed,\
    ITrashedProvidedBy


def trash(obj):
    providesITrashed(obj)


def restore(obj):
    noLongerProvidesITrashed(obj)


def is_trashed(obj):
    return ITrashedProvidedBy(obj)