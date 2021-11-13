from uuid import uuid4

def new_taskid():
    """
    Return a UUID string
    """
    return str(uuid4())