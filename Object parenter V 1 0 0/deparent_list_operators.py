import bpy
from .properties import *
from .utils import *


class OT_Dropdown_Add_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.dropdown_add_exile_entry"
    bl_label = "Add Exile Entry by Dropdown"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #hold selected dropdown option value 
    option: bpy.props.StringProperty()
        
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        object_pick = context.scene.objects[self.option]  #access existing object in the active scene
        
        #add new entry
        new_entry = snip_snip.objects_list.add() 
        #insert object data
        new_entry.object_name = self.option           #identifier string name
        new_entry.object_type = object_pick.type
        #place new entry via index
        snip_snip.object_idx = len(snip_snip.objects_list)-1
        
        return {"FINISHED"}
        
        
class OT_Add_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.add_exile_entry"
    bl_label = "Add Exile Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        obj = context.active_object
       
        #guard method to prevent duplicate entries
        if not exile_entry_exists(snip_snip.objects_list, obj.name):
            #add new entry
            new_entry = snip_snip.objects_list.add() 
            #insert object data
            new_entry.object_name = obj.name
            new_entry.object_type = obj.type
            #place new entry via index
            snip_snip.object_idx = len(snip_snip.objects_list)-1
            
            return {"FINISHED"}
        else:
            self.report({'INFO'}, "The item already exists")
            return {"CANCELLED"}
  
  
class OT_Mass_Add_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_add_exile_entry"
    bl_label = "Add More Exile Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip 
        
        for each_obj in context.selected_objects:
            if not exile_entry_exists(snip_snip.objects_list, each_obj.name):
                #add new entry
                new_entry = snip_snip.objects_list.add() 
                #insert object data
                new_entry.object_name = each_obj.name
                new_entry.object_type = each_obj.type
                #place new entry via index
                snip_snip.object_idx = len(snip_snip.objects_list)-1 
               
        return {"FINISHED"} 
  
    
class OT_Remove_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.remove_exile_entry"
    bl_label = "Remove Exile Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip
        return True if len(snip_snip.objects_list) > 0 else False

    def execute(self, context):
        snip_snip = context.scene.snip_snip
        #remove entry by indice
        snip_snip.objects_list.remove(snip_snip.object_idx)
        #make index point to next entry 
        snip_snip.object_idx = min(snip_snip.object_idx, len(snip_snip.objects_list)-1)

        return {"FINISHED"}


class OT_Clear_Exile_List(bpy.types.Operator):
    bl_idname = "my_operator.clear_exile_list"
    bl_label = "Clear Exile List"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip 
        return True if snip_snip.objects_list else False

    def execute(self, context):
        snip_snip = context.scene.snip_snip
        #clear list
        snip_snip.objects_list.clear() 
        #reset index
        snip_snip.object_idx = 0

        return {"FINISHED"}


class OT_Mass_Remove_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.mass_remove_exile_entry"
    bl_label = "Remove More Exile Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip
        return True if len(snip_snip.objects_list) > 0 else False

    def execute(self, context):
        snip_snip = context.scene.snip_snip
        
        #loop backwards to avoid index shifting issues
        for idx in reversed(range(len(snip_snip.objects_list))):
            
            #get entry by indice
            solo_obj = snip_snip.objects_list[idx]
            
            #check if object priority checkbox is clicked
            if solo_obj.object_priority == True:
            
                #remove this entry as its no longer needed
                snip_snip.objects_list.remove(idx)
    
                #make index point to next entry 
                snip_snip.object_idx = min(idx, len(snip_snip.objects_list)-1)
        
        return {"FINISHED"} 
      
    
class OT_Move_Exile_Entry_Up(bpy.types.Operator):
    bl_idname = "my_operator.move_exile_entry_up"
    bl_label = "Ascend Exile Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        #move entry up to indice A - 1. above
        snip_snip.objects_list.move(snip_snip.object_idx, snip_snip.object_idx - 1) 
        
        #make list point to moved entry
        snip_snip.object_idx = max(0, snip_snip.object_idx - 1)
         
        return {"FINISHED"}
        
        
class OT_Move_Exile_Entry_Down(bpy.types.Operator):
    bl_idname = "my_operator.move_exile_entry_down"
    bl_label = "Descend Exile Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        #move entry down to indice A + 1. above
        snip_snip.objects_list.move(snip_snip.object_idx, snip_snip.object_idx + 1) 
        
        #make list point to moved entry
        snip_snip.object_idx = min(snip_snip.object_idx + 1, len(snip_snip.objects_list) - 1)

        return {"FINISHED"}
    
### rename op here
class OT_Rename_Exile_Entry(bpy.types.Operator):
    bl_idname = "my_operator.rename_exile_entry"
    bl_label = "Rename Exile Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
       
        #get parent entry name
        object_name = snip_snip.objects_list[snip_snip.object_idx].object_name
    
        #access existing object in the active scene
        obj = context.scene.objects[object_name]
        
        #rename
        obj.name = snip_snip.object_rename 
        
        #edit active entry name
        snip_snip.objects_list[snip_snip.object_idx].object_name = snip_snip.object_rename
        
        return {"FINISHED"}
    
    
classes = [
           
OT_Dropdown_Add_Exile_Entry,
OT_Add_Exile_Entry,
OT_Mass_Add_Exile_Entry,
OT_Remove_Exile_Entry,
OT_Clear_Exile_List,
OT_Mass_Remove_Exile_Entry,
OT_Move_Exile_Entry_Up,
OT_Move_Exile_Entry_Down,
OT_Rename_Exile_Entry,
           
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()