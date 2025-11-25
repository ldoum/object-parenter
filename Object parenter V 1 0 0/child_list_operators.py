import bpy
from .properties import *
from .utils import *

  
class OT_Dropdown_Add_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.dropdown_add_child_entry"
    bl_label = "Add Child Entry by Dropdown"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #hold selected dropdown option value 
    option: bpy.props.StringProperty()
        
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #access existing object in the active scene
        object_pick = context.scene.objects[self.option]  
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]
    
        #add new subentry
        new_subentry = parent.children_list.add()
        #insert object data
        new_subentry.child_name = self.option
        new_subentry.child_type = object_pick.type
        #point to new entry
        parent.child_idx = len(parent.children_list)-1
            
        return {"FINISHED"}
        
        
class OT_Add_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.add_child_entry"
    bl_label = "Add Child Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        obj = context.active_object
        #get active parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        
        #child guard to check validity
        if not obj_follows_parenting_rules(obj, parent.parent_name):
            self.report({'INFO'}, "Can't assign this object as a child")
            return {"CANCELLED"}
        
        #guard method to prevent duplicate entries
        if not child_entry_exists_in_active_parent(pine_tree.parents_list, obj.name):
            #add new subentry
            new_subentry = parent.children_list.add() 
            #insert object data
            new_subentry.child_name = obj.name
            new_subentry.child_type = obj.type
            #point to new entry
            parent.child_idx = len(parent.children_list)-1
          
            return {"FINISHED"}
        else:
            self.report({'INFO'}, "The item already exists")
            return {"CANCELLED"}
    

class OT_Mass_Add_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_add_child_entry"
    bl_label = "Add More Child Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree 
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        
        for each_obj in context.selected_objects:
              
            #guard method to prevent duplicate entries
            if not child_entry_exists_in_active_parent(pine_tree.parents_list, each_obj.name):
                
                #child filter to check validity
                if obj_follows_parenting_rules(each_obj, parent.parent_name):
                    #add new subentry
                    new_subentry = parent.children_list.add() 
                    #insert object data
                    new_subentry.child_name = each_obj.name
                    new_subentry.child_type = each_obj.type
                    #point to new entry
                    parent.child_idx = len(parent.children_list)-1
            
        return {"FINISHED"}  
  
    
class OT_Remove_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.remove_child_entry"
    bl_label = "Remove Child Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        return True if len(parent.children_list) > 0 else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree 
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]

        #remove entry by indice
        parent.children_list.remove(parent.child_idx)
        #make index point to next entry 
        parent.child_idx = min(parent.child_idx, len(parent.children_list)-1)
        
        return {"FINISHED"}


class OT_Clear_Child_List(bpy.types.Operator):
    bl_idname = "my_operator.clear_child_list"
    bl_label = "Clear Child List"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        return True if parent.children_list else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree 
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]

        #clear list for parent entry
        parent.children_list.clear() 
        #reset index
        parent.child_idx = 0

        return {"FINISHED"}
 
 #### mass subtract op
class OT_Mass_Remove_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_remove_child_entry"
    bl_label = "Remove More Child Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_tree = context.scene.pine_tree
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        return True if len(parent.children_list) > 0 else False

    def execute(self, context):
        pine_tree = context.scene.pine_tree 
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        
        #loop backwards to avoid index shifting issues
        for idx in reversed(range(len(parent.children_list))):
            
            #get entry by indice
            sub_obj = parent.children_list[idx]
            
            #check if object priority checkbox is clicked
            if sub_obj.child_priority == True:
            
                #remove this entry as its no longer needed
                parent.children_list.remove(idx)
    
                #make index point to next entry 
                parent.child_idx = min(idx, len(parent.children_list)-1)
        
        return {"FINISHED"}    
    
    
class OT_Move_Child_Entry_Up(bpy.types.Operator):
    bl_idname = "my_operator.move_child_entry_up"
    bl_label = "Ascend Child Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]

        #move entry up to indice A - 1. above
        parent.children_list.move(parent.child_idx, parent.child_idx - 1) 
        #make list point to moved entry
        parent.child_idx = max(0, parent.child_idx - 1)  
        
        return {"FINISHED"}
        
        
class OT_Move_Child_Entry_Down(bpy.types.Operator):
    bl_idname = "my_operator.move_child_entry_down"
    bl_label = "Descend Child Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]

        #move entry up to indice A + 1. above
        parent.children_list.move(parent.child_idx, parent.child_idx + 1) 
        #make list point to moved entry
        parent.child_idx = min(parent.child_idx + 1, len(parent.children_list) - 1)
        
        return {"FINISHED"}
    
### rename op here

class OT_Rename_Child_Entry(bpy.types.Operator):
    bl_idname = "my_operator.rename_child_entry"
    bl_label = "Rename Child Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
         
        #get parent entry
        parent = pine_tree.parents_list[pine_tree.parent_idx]
        #then get child name
        child_name = parent.children_list[parent.child_idx].child_name
        
        #access existing object in the active scene
        obj = context.scene.objects[child_name] 
        #rename
        obj.name = parent.child_rename 
        #edit active entry name
        parent.children_list[parent.child_idx].child_name = parent.child_rename
        
        return {"FINISHED"}


classes = [
    
OT_Dropdown_Add_Child_Entry,
OT_Add_Child_Entry,
OT_Mass_Add_Child_Entry,
OT_Remove_Child_Entry,
OT_Clear_Child_List,
OT_Mass_Remove_Child_Entry,
OT_Move_Child_Entry_Up,
OT_Move_Child_Entry_Down,
OT_Rename_Child_Entry,
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()