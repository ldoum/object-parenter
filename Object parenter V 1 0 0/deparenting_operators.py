import bpy
from .properties import *
from .core import deparent_each_object


class OT_Deparent_The_Entry(bpy.types.Operator):
    bl_idname = "my_operator.deparent_one_entry"
    bl_label = "Deparent One Object"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip
        return True if snip_snip.objects_list else False
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        
        #get active object
        active_exile_object = snip_snip.objects_list[snip_snip.object_idx]
      
        #call this method for deparenting active object 
        deparent_each_object(active_exile_object.object_name)
             
        #remove this active entry as its no longer needed
        snip_snip.objects_list.remove(snip_snip.object_idx)
        
        #make index point to next entry 
        snip_snip.object_idx = min(snip_snip.object_idx, len(snip_snip.objects_list)-1)

        return {"FINISHED"}


class OT_Deparent_Priority_Only(bpy.types.Operator):
    bl_idname = "my_operator.deparent_priority"
    bl_label = "Deparent By Custom Selection"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip
        return True if snip_snip.objects_list else False
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        
        #loop backwards to avoid index shifting issues
        for idx in reversed(range(len(snip_snip.objects_list))):
            
            #get entry by indice
            solo_obj = snip_snip.objects_list[idx]
            
            #check if object priority checkbox is clicked
            if solo_obj.object_priority == True:
            
                #call this method for deparenting active object
                deparent_each_object(solo_obj.object_name)
                
                #remove this entry as its no longer needed
                snip_snip.objects_list.remove(idx)
    
                #make index point to next entry 
                snip_snip.object_idx = min(idx, len(snip_snip.objects_list)-1)

        return {"FINISHED"}


class OT_Deparent_All_Entries(bpy.types.Operator):
    bl_idname = "my_operator.deparent_entries"
    bl_label = "Deparent All Objects"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        snip_snip = context.scene.snip_snip
        return True if snip_snip.objects_list else False
    
    def execute(self, context):
        snip_snip = context.scene.snip_snip
        
        #get each element and run this function
        for solo_obj in snip_snip.objects_list:
            deparent_each_object(solo_obj.object_name)
        
        #dump the list as its no longer needed
        snip_snip.objects_list.clear()
        
        return {"FINISHED"}

classes = [
    
OT_Deparent_The_Entry,
OT_Deparent_Priority_Only,
OT_Deparent_All_Entries,    
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()