import bpy
from .utils import *

### helper functions [9]
def active_parent_object_by_idx(self, context):
    pine_tree = context.scene.pine_tree
       
    #get parent entry name
    parent_name = pine_tree.parents_list[pine_tree.parent_idx].parent_name
    
    #get if object exists
    obj = context.scene.objects.get(parent_name)

    if obj:
        # Deselect all other objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        #select the object
        obj.select_set(True)
        #make it active
        context.view_layer.objects.active = obj


def active_child_object_by_idx(self, context):
    pine_tree = context.scene.pine_tree
       
    #get active parent entry name
    parent_active = pine_tree.parents_list[pine_tree.parent_idx]
    
    #get parent entry name
    child_name = parent_active.children_list[parent_active.child_idx].child_name
    
    #get if object exists
    obj = context.scene.objects.get(child_name)

    if obj:
        # Deselect all other objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        #select the object
        obj.select_set(True)
        #make it active
        context.view_layer.objects.active = obj


def active_exile_object_by_idx(self, context):
    snip_snip = context.scene.snip_snip
       
    #get parent entry name
    object_name = snip_snip.objects_list[snip_snip.object_idx].object_name
    
    #get if object exists
    obj = context.scene.objects.get(object_name)

    if obj:
        # Deselect all other objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        #select the object
        obj.select_set(True)
        #make it active
        context.view_layer.objects.active = obj


### generate items for dynamic dropdowns

def list_of_parent_objects(self, context):
    
    items = []
    
    pine_tree = context.scene.pine_tree
    
    for obj in context.scene.objects: 
        
        #check if name already exists in the parent list. If so, dont append
        if not parent_entry_exists(pine_tree.parents_list, obj.name):
     
            items.append((obj.name, obj.name, ""))
    
    #if items is full
    if items: 
        return items
    else:
        return [("NOTHING", "No items here", "")]
        
    
def list_of_exile_objects(self, context):
    
    items = []
    
    snip_snip = context.scene.snip_snip
    
    for obj in context.scene.objects: 
        
        #check if name already exists in the parent list. If so, dont append
        if not exile_entry_exists(snip_snip.objects_list, obj.name):
     
            items.append((obj.name, obj.name, ""))
    
    #if items is full
    if items: 
        return items
    else:
        return [("NOTHING", "No items here", "")]
    

def list_of_child_objects(self, context):
    
    items = []
    
    pine_tree = context.scene.pine_tree
    #get active parent name
    the_base_obj_name = pine_tree.parents_list[pine_tree.parent_idx].parent_name
    
    for obj in context.scene.objects: 
        
        #check if child object is already taken
        if not child_entry_exists_in_active_parent(pine_tree.parents_list, obj.name):
                    
            #child filter
            if obj_follows_parenting_rules(obj, the_base_obj_name):   
                
                items.append((obj.name, obj.name, ""))
    
    #if items is full
    if items: 
        return items
    else:
        return [("NOTHING", "No items here", "")]
    

### pass selected item from the dynamic dropdowns into ops while running them   
def send_the_child_object_enum(self, context):    
    bpy.ops.my_operator.dropdown_add_child_entry(option=self.child_dropdown)


def send_the_object_enum(self, context):    
    bpy.ops.my_operator.dropdown_add_parent_entry(option=self.parent_dropdown)   


def send_the_exiled_object_enum(self, context):    
    bpy.ops.my_operator.dropdown_add_exile_entry(option=self.object_dropdown)     
        
        
### parenting object data
class ChildObjectSubEntry(bpy.types.PropertyGroup):
    child_name: bpy.props.StringProperty(name="Child Name")
    child_type: bpy.props.StringProperty(name="Child Type")
    child_priority: bpy.props.BoolProperty(name="Priority", default=False)
    
    
class ParentObjectEntry(bpy.types.PropertyGroup):
    parent_name: bpy.props.StringProperty(name="Parent Name")
    parent_type: bpy.props.StringProperty(name="Parent Type")
    parent_priority: bpy.props.BoolProperty(name="Priority", default=False)
    children_list: bpy.props.CollectionProperty(type=ChildObjectSubEntry)
    child_idx: bpy.props.IntProperty(
                name="Active Index for Child", 
                default=0,
                update=active_child_object_by_idx,
                )
    child_rename: bpy.props.StringProperty(name="New Child Name")
    child_dropdown: bpy.props.EnumProperty(
                    name="Child",
                    items=list_of_child_objects,
                    update=send_the_child_object_enum,
                    )  
         
         
class ParentingTreeData(bpy.types.PropertyGroup):    
    parents_list: bpy.props.CollectionProperty(type=ParentObjectEntry)
    parent_idx: bpy.props.IntProperty(
                name="Active Index for Parent", 
                default=0,
                update=active_parent_object_by_idx,
                )
    parent_rename: bpy.props.StringProperty(
                    name="New Parent Name",
    )
    parent_dropdown: bpy.props.EnumProperty(
                    name="Parent",
                    items=list_of_parent_objects,
                    update=send_the_object_enum,
                    ) 
    
    
### deparenting object data
class DeparentObjectEntry(bpy.types.PropertyGroup):
    object_name: bpy.props.StringProperty(
                name="Parent Name",
                )
    object_type: bpy.props.StringProperty(name="Parent Type")
    object_priority: bpy.props.BoolProperty(name="Priority", default=False)
    
    
class DeparentingObjectData(bpy.types.PropertyGroup):    
    objects_list: bpy.props.CollectionProperty(type=DeparentObjectEntry)
    object_idx: bpy.props.IntProperty(
                name="Active Index for Exile Object", 
                default=0,
                update=active_exile_object_by_idx,
                )
    object_rename: bpy.props.StringProperty(
                    name="New Object Name",
    )   
    object_dropdown: bpy.props.EnumProperty(
                    name="Exile obj",
                    items=list_of_exile_objects,
                    update=send_the_exiled_object_enum,
                    )
          
          
### class serves to hold dropdowns
class AccessoryData(bpy.types.PropertyGroup):  
    mode_dropdown: bpy.props.EnumProperty(
                    name="Switch",
                    items=[
                        ("PARENT","Parent","Set mode to parent"),
                        ("DEPARENT","Deparent","Set mode to deparent"),
                    ],
                    default="PARENT"
                    ) 
    show_names: bpy.props.BoolProperty(
                    name="Show names?",
                    default=False,
                    )                

classes = [
    
#data for parent and child lists
ChildObjectSubEntry, #L3
ParentObjectEntry,   #L2
ParentingTreeData,   #L1

#data for deparent lists
DeparentObjectEntry,    #L2
DeparentingObjectData,  #L1

#data for all Accessories.
AccessoryData,
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()