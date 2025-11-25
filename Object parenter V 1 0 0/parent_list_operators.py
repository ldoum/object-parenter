import bpy
from .properties import *
from .utils import *


class OT_Dropdown_Add_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.dropdown_add_parent_entry"
    bl_label = "Add Parent Entry by Dropdown"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #hold selected dropdown option value 
    option: bpy.props.StringProperty()
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        object_pick = context.scene.objects[self.option]  #access existing object in the active scene
        
        new_entry = pine_tree.parents_list.add() 
        #insert object data
        new_entry.parent_name = self.option     #identifier string name
        new_entry.parent_type = object_pick.type
        #point to new entry
        pine_tree.parent_idx = len(pine_tree.parents_list)-1
        
        return {"FINISHED"}
        
        
class OT_Add_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.add_parent_entry"
    bl_label = "Add Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        obj = context.active_object
       
        #guard method to prevent duplicate entries
        if not parent_entry_exists(pine_tree.parents_list, obj.name):
            #add new entry
            new_entry = pine_tree.parents_list.add() 
            #insert object data
            new_entry.parent_name = obj.name
            new_entry.parent_type = obj.type
            #place new entry via index
            pine_tree.parent_idx = len(pine_tree.parents_list)-1

            return {"FINISHED"}
        else:
            self.report({'INFO'}, "The item already exists")
            return {"CANCELLED"}

  
class OT_Mass_Add_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_add_parent_entry"
    bl_label = "Add More Parent Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        for each_obj in context.selected_objects:
            
            if not parent_entry_exists(pine_tree.parents_list, each_obj.name):
                #add new entry
                new_entry = pine_tree.parents_list.add() 
                #insert object data
                new_entry.parent_name = each_obj.name
                new_entry.parent_type = each_obj.type
                #place new entry via index
                pine_tree.parent_idx = len(pine_tree.parents_list)-1 

        return {"FINISHED"}


class OT_Remove_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.remove_parent_entry"
    bl_label = "Remove Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree
        return True if len(pine_tree.parents_list) > 0 else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #remove entry by indice
        pine_tree.parents_list.remove(pine_tree.parent_idx)
        
        #make index point to next entry 
        pine_tree.parent_idx = min(pine_tree.parent_idx, len(pine_tree.parents_list)-1)

        return {"FINISHED"}


class OT_Clear_Parent_List(bpy.types.Operator):
    bl_idname = "my_operator.clear_parent_list"
    bl_label = "Clear Parent List"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree 
        return True if pine_tree.parents_list else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #clear list
        pine_tree.parents_list.clear() 
        #reset index
        pine_tree.parent_idx = 0

        return {"FINISHED"}

#### mass subtract op
class OT_Mass_Remove_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_remove_parent_entry"
    bl_label = "Remove More Parent Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree
        return True if len(pine_tree.parents_list) > 0 else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #loop backwards to avoid index shifting issues
        for idx in reversed(range(len(pine_tree.parents_list))):
            
            #get entry by indice
            base_obj = pine_tree.parents_list[idx]
            
            #check if object priority checkbox is clicked
            if base_obj.parent_priority == True:
            
                #remove this entry as its no longer needed
                pine_tree.parents_list.remove(idx)
    
                #make index point to next entry 
                pine_tree.parent_idx = min(idx, len(pine_tree.parents_list)-1)
        
        ###########################
        
                
        return {"FINISHED"}     
    
class OT_Move_Parent_Entry_Up(bpy.types.Operator):
    bl_idname = "my_operator.move_parent_entry_up"
    bl_label = "Ascend Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #move entry up to indice A - 1. above
        self.parent_list.move(self.parent_idx, self.parent_idx - 1) 
        
        #make list point to moved entry
        self.parent_idx = max(0, self.parent_idx - 1)
        
        return {"FINISHED"}
        
        
class OT_Move_Parent_Entry_Down(bpy.types.Operator):
    bl_idname = "my_operator.move_parent_entry_down"
    bl_label = "Descend Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #move entry down to indice A + 1. above
        pine_tree.parent_list.move(pine_tree.parent_idx, pine_tree.parent_idx + 1) 
        
        #make list point to moved entry
        pine_tree.parent_idx = min(pine_tree.parent_idx + 1, len(pine_tree.parents_list) - 1)

        return {"FINISHED"}
    
### rename op here    

class OT_Rename_Parent_Entry(bpy.types.Operator):
    bl_idname = "my_operator.rename_parent_entry"
    bl_label = "Rename Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #get parent entry name
        parent_name = pine_tree.parents_list[pine_tree.parent_idx].parent_name
    
        #access existing object in the active scene
        obj = context.scene.objects[parent_name]
        #rename
        obj.name = pine_tree.parent_rename 
        #edit active entry name
        pine_tree.parents_list[pine_tree.parent_idx].parent_name = pine_tree.parent_rename
        
        return {"FINISHED"}


classes = [

OT_Dropdown_Add_Parent_Entry,
OT_Add_Parent_Entry,
OT_Mass_Add_Parent_Entry,
OT_Remove_Parent_Entry,
OT_Clear_Parent_List,
OT_Mass_Remove_Parent_Entry,
OT_Move_Parent_Entry_Up,
OT_Move_Parent_Entry_Down,
OT_Rename_Parent_Entry,

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()