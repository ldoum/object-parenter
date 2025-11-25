
#circular parenting guard. No upward loops.  
def ancestor_obj_is_found_in_chain(start_obj, potential_ancenstor_name):
   
    #start off with the parent
    current_object = start_obj.parent
        
    #run this loop until the value is None
    while current_object:
            
        #if name matches, then the new child object is the ancestor of the parenting chain
        if current_object.name == potential_ancenstor_name:
            return True
        
        #if not a match, go to the parent and make that the current obj
        current_object = current_object.parent
        
    return False 


#circular parenting guard. No downward loops. 
def descendant_obj_is_found_in_chain(start_obj, potential_descendant_name):
    
    #start off with generation 2. 
    stack = list(start_obj.children)
   
    #run this loop until the value is None
    while stack:
        
        child = stack.pop() #pop last element out and isolate it
        
        #if name matches, then the new child object is the descendant of the parenting chain    
        if child.name == potential_descendant_name:
            return True
        
        stack.extend(child.children) #add children of last element if any. otherwise, move on.
        
    return False 


#child guard
def obj_follows_parenting_rules(child_obj, parent_obj_name):
    
    #only allow objects w/o parents to be parented
    if child_obj.parent:
        return False
    
    #if active parent object is also the child (self assignment)
    if child_obj.name == parent_obj_name:
        return False

    #if child to assign is the ancestor of active parent object
    if ancestor_obj_is_found_in_chain(child_obj, parent_obj_name):
        return False
    
    #if child to assign is the descendant of active parent object
    if descendant_obj_is_found_in_chain(child_obj, parent_obj_name):
        return False
    
    #if all rules are followed
    return True


#claimed entry guard. scan entire data structure. stop loop if the entry is already there
def child_entry_exists_in_active_parent(parent_collection, obj_name):
    for main_obj in parent_collection:
        for sub_obj in main_obj.children_list: 
            if obj_name == sub_obj.child_name:    
                return True
    return False        
    
    
#duplicate entry guards. flips through history of the list, stop loop if the match is found    
def parent_entry_exists(collection, obj_name):
    for item in collection:                   
        if item.parent_name == obj_name:      
            return True
    return False                          


def exile_entry_exists(collection, obj_name):
    for item in collection:                  
        if item.object_name == obj_name:      
            return True
    return False 