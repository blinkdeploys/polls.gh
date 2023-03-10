import os
import uuid
import random
from datetime import datetime 
from django.core.serializers.json import DjangoJSONEncoder


def intify(value) -> int:
    if type(value) is int:
        value = value
    elif type(value) is str:
        value = int(value)
    else:
        value = 0
    return value

def snakeify(title, remove_special=True):
    if type(title) is str:
        title = title.lower().replace(' ', '_').replace('.', '')
        if remove_special:
            remove = ['+','-','=','!','~','`','*','|','"','\'','$','%','^','&','@','{','}','[',']',';',',','.','<','>','?','@','&','*','(',')','\/','/']
            for c in remove:
                title = title.replace(c, '')
        return title
    return ''

def upload_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.now()

    # set the complete filename, path and extension
    path = "results{}{}{}/".format(todays_date.year, todays_date.month, todays_date.day)
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))

    # Filename reformat
    filename_reformat = stringId + randInt + extension

    return os.path.join(path, filename_reformat)

# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, YourCustomType):
#             return str(obj)
#         return super().default(obj)

