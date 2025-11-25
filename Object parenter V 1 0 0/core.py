import bpy

def assign_children_to_parent(parent_name, bunch_of_child_names):
    
    #access this object 
    parent_ = bpy.context.scene.objects.get(parent_name)
         
    #if child list isnt empty and the parent object exists
    if bunch_of_child_names and parent_:   
             
        #scroll through all children by name
        for each_obj in bunch_of_child_names:  
                                                         
            child_ = bpy.data.objects.get(each_obj) #get each child
             
            #if child exists:
            if child_: 
                     
                #parent this object                     
                child_.parent = parent_   
            
                #keep transform                                      
                child_.matrix_parent_inverse = parent_.matrix_world.inverted()  


def deparent_each_object(this_obj):
    #access this object 
    child_ = bpy.context.scene.objects.get(this_obj)
    
    #if child exists:
    if child_:
             
        #deparent this object    
        child_.parent = None
    
        #keep transform                                  
        child_.matrix_world = child_.matrix_world.copy()      
    