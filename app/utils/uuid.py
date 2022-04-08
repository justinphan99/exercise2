import uuid

def isValidUUID(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False