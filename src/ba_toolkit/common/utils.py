import re


def find_meshes(root_obj, pattern=None):
    found = []

    def _search(obj):
        if obj.type == 'MESH':
            name = obj.name
            if (pattern is None) or (pattern and re.search(pattern, name)):
                found.append(obj)
        for child in obj.children:
            _search(child)

    _search(root_obj)
    return found
