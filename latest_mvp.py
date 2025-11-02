import bpy

def assign_children_to_parent(choose):
  
    parent_ = bpy.data.objects.get(choose["parent_name"])       #get each parent within parenter_chain list
  
    #if child list isnt empty and parent object exists
    if choose["child_names"] and parent_:
        
        #scroll through all children by name
        for i in range(len(choose["child_names"])):
    
            child_ = bpy.data.objects.get(choose["child_names"][i])               #get each child
            
            #if a child exists:
            if child_:
                child_.parent = parent_                                          #parent child object to main object                              
                child_.matrix_parent_inverse = parent_.matrix_world.inverted()   #keep transform when parenting


def deparent_children(name):
    
    child_ = bpy.data.objects.get(name)                 #get child by name
  
    #if child exists:
    if child_:
        child_.parent = None                             #deparent this object
        child_.matrix_world = child_.matrix_world.copy() #keep transform when deparenting


def deparent_children_batch(this_obj):
    child_ = bpy.data.objects[this_obj.name]            #access this object it expects to exist
    child_.parent = None                                #deparent this object
    child_.matrix_world = child_.matrix_world.copy()    #keep transform when deparenting
    
def main():
    
    code = 2  #change this value to set mode
    
    match code:
        
        case 0:
            """
            {
            "parent_name": "", 
            "child_names": ["",""],
            },
            """
            #populate this list
            parenter_chain = [
            {"parent_name": "Shvan92_Suspension", 
            "child_names": [
            "Shvan92_Brake_Rotor.L", 
            "Shvan92_Brake_Rotor.R", 
            "Shvan92_Suspension_Front",  
            "Shvan92_Suspension_Rear_Leaf_Spring"
            ]}, 
            {"parent_name": "Shvan92_WheelCustom_FL", 
            "child_names": ["Shvan92_Wheel_FL"]}, 
            {"parent_name": "Shvan92_WheelCustom_FR", 
            "child_names": ["Shvan92_Wheel_FR"]}, 
            {"parent_name": "Shvan92_WheelCustom_RL", 
            "child_names": ["Shvan92_Wheel_RL"]}, 
            {"parent_name": "Shvan92_WheelCustom_RR", 
            "child_names": ["Shvan92_Wheel_RR"]}]
    
            for obj in parenter_chain:   #insert each object info dictionary into method
                assign_children_to_parent(obj)
        
        case 1:
            
            deparenter_chain = ["Cube.153","Cube.004"]
    
            for x in deparenter_chain:  #insert each object name into method
                deparent_children(x)
            
        case 2:
        
            for x in bpy.context.selected_objects:  #collect all selected objects and put each one into method
                deparent_children_batch(x)
                
        case _:
            
            pass

if __name__ == "__main__":
    main()    
