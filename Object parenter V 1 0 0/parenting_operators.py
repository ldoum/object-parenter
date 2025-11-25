import bpy
from .properties import *
from .core import assign_children_to_parent

class OT_Parent_The_Entry(bpy.types.Operator):
    bl_idname = "my_operator.parent_one_entry"
    bl_label = "Parent One Object"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #get active parent
        active_parent = pine_tree.parents_list[pine_tree.parent_idx]
        
        #temp list
        children_names = []
       
        #go through each child that isn't parented yet in children list
        for sub_obj in active_parent.children_list:
            
            #fill the temp list
            children_names.append(sub_obj.child_name) 
            
            #call this method for acctive parent object   
            assign_children_to_parent(active_parent.parent_name, children_names)
            
            #clear to avoid child name pile up
            children_names.clear()
        
        #remove this active entry as its no longer needed
        pine_tree.parents_list.remove(pine_tree.parent_idx)
        
        #make index point to next entry 
        pine_tree.parent_idx = min(pine_tree.parent_idx, len(pine_tree.parents_list)-1)
        
        return {"FINISHED"}


class OT_Parent_Priority_Only(bpy.types.Operator):
    bl_idname = "my_operator.parent_priority"
    bl_label = "Parent By Custom Selection"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #temp list
        children_names = []
       
        #go through each parent in main list
        #main_obj acts like pine_tree.parents_list[pine_tree.parent_idx]
        for idx in reversed(range(len(pine_tree.parents_list))):
            
            #get entry by indice
            main_obj = pine_tree.parents_list[idx]
            
            #check if parent priority checkbox is clicked
            if main_obj.parent_priority == True:
            
                #go through each child that isn't parented yet in children list
                for sub_obj in main_obj.children_list:
            
                    #fill the temp list
                    #sub_obj acts like main_obj.children_list[main_obj.child_idx]
                    children_names.append(sub_obj.child_name) 
                
                #call this method for each parent object   
                assign_children_to_parent(main_obj.parent_name, children_names)
            
                #clear to avoid child name pile up
                children_names.clear()
                
                #remove this entry as its no longer needed
                pine_tree.parents_list.remove(idx)
            
                #make index point to next entry 
                pine_tree.parent_idx = min(idx, len(pine_tree.parents_list)-1)
        
        return {"FINISHED"}
    

class OT_Parent_All_Entries(bpy.types.Operator):
    bl_idname = "my_operator.parent_entries"
    bl_label = "Parent All Objects"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_tree = context.scene.pine_tree
        
        #temp list
        children_names = []
       
        #go through each parent in main list
        #main_obj acts like pine_tree.parents_list[pine_tree.parent_idx]
        for main_obj in pine_tree.parents_list:
            
            #go through each child that isn't parented yet in children list
            for sub_obj in main_obj.children_list:
            
                #fill the temp list
                #sub_obj acts like main_obj.children_list[main_obj.child_idx]
                children_names.append(sub_obj.child_name) 
                
            #call this method for each parent object   
            assign_children_to_parent(main_obj.parent_name, children_names)
            
            #clear to avoid child name pile up
            children_names.clear()
            
        #finally, clear the entire parent list
        pine_tree.parents_list.clear()
  
        return {"FINISHED"}
    

classes = [
    
OT_Parent_The_Entry,
OT_Parent_Priority_Only,
OT_Parent_All_Entries,
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()