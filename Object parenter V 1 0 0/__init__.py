bl_info = {
    "name": "Object Parenter", 
    "blender": (2, 8, 0),
    "category": "Object",
    "author": "Lancine Doumbia", 
    "version": (1, 0, 1), 
    "location": "View3D > Sidebar", #important
    "description": "Automate the process of parenting and/or deparenting objects", 
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}

from . import properties, panels, lists, child_list_operators, parent_list_operators, deparent_list_operators, reveal_object_names_operator, parenting_operators, deparenting_operators

def register():
    properties.register()
    lists.register()
    panels.register()
    child_list_operators.register()
    parent_list_operators.register()
    deparent_list_operators.register()
    reveal_object_names_operator.register()
    parenting_operators.register()
    deparenting_operators.register()

def unregister():
    properties.unregister()
    lists.unregister()
    panels.unregister()
    child_list_operators.unregister()
    parent_list_operators.unregister()
    deparent_list_operators.unregister()
    reveal_object_names_operator.unregister()
    parenting_operators.unregister()
    deparenting_operators.unregister()

if __name__ == "__main__":

    register()
