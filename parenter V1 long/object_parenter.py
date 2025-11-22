import bpy
##############core###############################


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
    
    
##############core end###############################   

###############################UTILS #############################


# 6 utility functions


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

###############################UTILS END#############################

###############################PROPERTIES#############################

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
    
###############################PROPERTIES END#############################    


###############################LISTS#############################

class UL_Parent_History(bpy.types.UIList):
#UIList to show search history
    def draw_item(
        self, context, layout, data, item, icon,
        active_data, active_propname, index
        ):
        # item is a SearchEntry
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=f"{item.parent_name}")
            row.label(text=f"({item.parent_type})")
            row.prop(item, "parent_priority")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=f"{item.parent_name}")
            layout.label(text=f"({item.parent_type})")


class UL_Child_History(bpy.types.UIList):
#UIList to show search history
    def draw_item(
        self, context, layout, data, item, icon,
        active_data, active_propname, index
        ):
        # item is a SearchEntry
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=f"{item.child_name}")
            row.label(text=f"({item.child_type})")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=f"{item.child_name}")
            layout.label(text=f"({item.child_type})")


class UL_Object_History(bpy.types.UIList):
#UIList to show search history
    def draw_item(
        self, context, layout, data, item, icon,
        active_data, active_propname, index
        ):
        # item is a SearchEntry
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=f"{item.object_name}")
            row.label(text=f"({item.object_type})")
            row.prop(item, "object_priority")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=f"{item.object_name}")
            layout.label(text=f"({item.object_type})")

            
###############################LISTS EMD#############################


###############################OPERATORS #############################


### operators to manage parenting list

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
        
        for each_obj in context.selected_objects:
            
            #if entry for the object is there
            if parent_entry_exists(pine_tree.parents_list, each_obj.name):
                
                #scroll through the collection property list
                for idx in reversed(range(len(pine_tree.parents_list))):
                    
                    #get entry by indice
                    solo_obj = pine_tree.parents_list[idx]
                    
                    #if match
                    if each_obj.name == solo_obj.parent_name:
                        
                        pine_tree.parents_list.remove(idx)
                        
                        pine_tree.parent_idx = min(idx, len(pine_tree.parents_list)-1) 
                
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


### operators to manage child list   
   
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
        
        for each_obj in context.selected_objects:
            
            #if entry for the object is there
            if child_entry_exists_in_active_parent(pine_tree.parents_list, each_obj.name):
                
                #scroll through the collection property list
                for idx in reversed(range(len(parent.children_list))):
                    
                    #get entry by indice
                    solo_obj = parent.children_list[idx]
                    
                    #if match
                    if each_obj.name == solo_obj.child_name:
                        
                        parent.children_list.remove(idx)
                        
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

### operators to manage deparenting list  

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
        
        for each_obj in context.selected_objects:
            
            #if entry for the object is there
            if exile_entry_exists(snip_snip.objects_list, each_obj.name):
                
                #scroll through the collection property list
                for idx in reversed(range(len(snip_snip.objects_list))):
                    
                    #get entry by indice
                    solo_obj = snip_snip.objects_list[idx]
                    
                    #if match
                    if each_obj.name == solo_obj.object_name:
                        
                        snip_snip.objects_list.remove(idx)
                        
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
    
########################## deparent end

##### Tool
class OT_Reveal_Object_Names(bpy.types.Operator):
    bl_idname = "my_operator.reveal_names"
    bl_label = "Reveal Object Names"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        extra = context.scene.extra
   
        #apply
        for each_obj in context.selected_objects:
            
            if extra.show_names == True:
                each_obj.show_name = extra.show_names
            else:
                each_obj.show_name = extra.show_names
       
        return {"FINISHED"}


### CORE

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

          
###############################OPERATORS EMD#############################


###############################PANELS #############################


class PT_BasePanel(bpy.types.Panel):
    bl_idname = "panelname"
    bl_label = "List panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Parenter"
    
    #show up in object mode only
    @classmethod
    def poll(cls,context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout
        extra_stuff = context.scene.extra 
        assign_ = context.scene.pine_tree 
        disband_ = context.scene.snip_snip 
        
        ### accessory panel
        box = layout.box().row()
        box.prop(extra_stuff, "show_names")
        box.operator(OT_Reveal_Object_Names.bl_idname, text="Apply")
        
        layout.prop(extra_stuff, "mode_dropdown", expand=True)
        
        #switch windows. Parent window is default.
        if extra_stuff.mode_dropdown == "PARENT":
            
            #parent window
            layout.label(text="Parenting")
            
            #parent dropdown
            layout.prop(assign_, "parent_dropdown")
            
            #parent list
            layout.template_list(
                "UL_Parent_History", "", #List class name, list id
                assign_, "parents_list", # Collection property
                assign_, "parent_idx", # Active property
            )
            
            
            #parent object rename
            row = layout.row(align=True)
            row.prop(assign_, "parent_rename")
            row.operator(OT_Rename_Parent_Entry.bl_idname, text="", icon="CHECKMARK")
            
            #manage parent list
            row = layout.row(align=True)
            row.operator(OT_Add_Parent_Entry.bl_idname, text="+")
            row.operator(OT_Mass_Add_Parent_Entry.bl_idname, text="++")
            row.operator(OT_Remove_Parent_Entry.bl_idname, text="-")
            row.operator(OT_Mass_Remove_Parent_Entry.bl_idname, text="--")
            row.operator(OT_Clear_Parent_List.bl_idname, text="", icon="TRASH")
            row.operator(OT_Move_Parent_Entry_Up.bl_idname, text="", icon="TRIA_UP")
            row.operator(OT_Move_Parent_Entry_Down.bl_idname, text="", icon="TRIA_DOWN")
            
            #parent select button
            layout.operator(OT_Parent_Priority_Only.bl_idname, text="Parent Selected")
            
            
            #if parents list has something
            if assign_.parents_list:
                
                #access child subentry
                parent_active = assign_.parents_list[assign_.parent_idx]
                
                #retrieve name of active parent obj and access it
                main_obj = context.scene.objects.get(parent_active.parent_name)
                
                #check if object exists to avoid key errors for bpy_prop_collection
                if main_obj:
                    #if it has children, display the box
                    if main_obj.children:
                        layout.label(text=f"Children of {parent_active.parent_name}:")
                        #show children already added
                        box = layout.box()
                        for child in main_obj.children:
                            box.label(text=f"{child.name}")
                else:
                    box = layout.box()
                    box.label(text=f"This object can't be found.")
                    
                #check if invisible
                if not main_obj.visible_get():
                    box = layout.box()
                    box.label(text=f"This object is invisible.")
                
                #child dropdown
                layout.prop(parent_active, "child_dropdown")
            
            
                #child list
                layout.template_list(
                    "UL_Child_History", "", #List class name, list id
                    parent_active, "children_list", # Collection property
                    parent_active, "child_idx", # Active property
                )
                
                #child object rename
                row = layout.row(align=True)
                row.prop(parent_active, "child_rename")
                row.operator(OT_Rename_Child_Entry.bl_idname, text="", icon="CHECKMARK")
                
                #only prompt if children list is full
                if parent_active.children_list:
                    
                    sub = parent_active.children_list[parent_active.child_idx]
                        
                    sub_obj = context.scene.objects.get(sub.child_name)
                    
                    #prompt if child object cant be found    
                    if not sub_obj:
                        box = layout.box()
                        box.label(text=f"This object can't be found.")
                        
                    #check if invisible
                    if not sub_obj.visible_get():
                        box = layout.box()
                        box.label(text=f"This object is invisible.")
                
                #manage child list
                row = layout.row(align=True)
                row.operator(OT_Add_Child_Entry.bl_idname, text="+")
                row.operator(OT_Mass_Add_Child_Entry.bl_idname, text="++")
                row.operator(OT_Remove_Child_Entry.bl_idname, text="-")
                row.operator(OT_Mass_Remove_Child_Entry.bl_idname, text="--")
                row.operator(OT_Clear_Child_List.bl_idname, text="", icon="TRASH")
                row.operator(OT_Move_Child_Entry_Up.bl_idname, text="", icon="TRIA_UP")
                row.operator(OT_Move_Child_Entry_Down.bl_idname, text="", icon="TRIA_DOWN")
                
                row = layout.row(align=True)
                row.operator(OT_Parent_The_Entry.bl_idname, text="Parent")
                row.operator(OT_Parent_All_Entries.bl_idname, text="Parent All")
        else:
            
            #deparent window
            layout.label(text="Deparenting")
            
            #parent dropdown
            layout.prop(disband_, "object_dropdown")
            
            #deparent list
            layout.template_list(
                "UL_Object_History", "", #List class name, list id
                disband_, "objects_list", # Collection property
                disband_, "object_idx", # Active property
            )
            
            
            #exile object rename
            row = layout.row(align=True)
            row.prop(disband_, "object_rename")
            row.operator(OT_Rename_Exile_Entry.bl_idname, text="", icon="CHECKMARK")
            
            #manage exile list
            row = layout.row(align=True)
            row.operator(OT_Add_Exile_Entry.bl_idname, text="+")
            row.operator(OT_Mass_Add_Exile_Entry.bl_idname, text="++")
            row.operator(OT_Remove_Exile_Entry.bl_idname, text="-")
            row.operator(OT_Mass_Remove_Exile_Entry.bl_idname, text="--")
            row.operator(OT_Clear_Exile_List.bl_idname, text="", icon="TRASH")
            row.operator(OT_Move_Exile_Entry_Up.bl_idname, text="", icon="TRIA_UP")
            row.operator(OT_Move_Exile_Entry_Down.bl_idname, text="", icon="TRIA_DOWN")
            
            #exile select button
            layout.operator(OT_Deparent_Priority_Only.bl_idname, text="Deparent Selected")
            
            #prompt if exile object cant be found
            if disband_.objects_list:
                
                #access child subentry
                exile_active = disband_.objects_list[disband_.object_idx]
                
                exile_obj = context.scene.objects.get(exile_active.object_name)
                        
                if not exile_obj:
                    box = layout.box()
                    box.label(text=f"This object can't be found.")
                    
                #check if invisible
                if not exile_obj.visible_get():
                    box = layout.box()
                    box.label(text=f"This object is invisible.")
                
            row = layout.row(align=True)
            row.operator(OT_Deparent_The_Entry.bl_idname, text="Deparent")
            row.operator(OT_Deparent_All_Entries.bl_idname, text="Deparent All")
            
        

###############################PANELS EMD#############################

#33 ops



##############################REGISTRATION#############################

classes = [

#data for parent and child lists
ChildObjectSubEntry,
ParentObjectEntry,
ParentingTreeData,

#data for deparent lists
DeparentObjectEntry,
DeparentingObjectData,

#data for all Accessories.
AccessoryData,

#tool to show object names
OT_Reveal_Object_Names,


#define entry panel for each list.
UL_Parent_History,
UL_Child_History,
UL_Object_History,


#ops for parent list
OT_Dropdown_Add_Parent_Entry,
OT_Add_Parent_Entry,
OT_Mass_Add_Parent_Entry,
OT_Remove_Parent_Entry,
OT_Clear_Parent_List,
OT_Mass_Remove_Parent_Entry,
OT_Move_Parent_Entry_Up,
OT_Move_Parent_Entry_Down,
OT_Rename_Parent_Entry,

#ops for child list
OT_Dropdown_Add_Child_Entry,
OT_Add_Child_Entry,
OT_Mass_Add_Child_Entry,
OT_Remove_Child_Entry,
OT_Clear_Child_List,
OT_Mass_Remove_Child_Entry,
OT_Move_Child_Entry_Up,
OT_Move_Child_Entry_Down,
OT_Rename_Child_Entry,


#ops for deparent list
OT_Dropdown_Add_Exile_Entry,
OT_Add_Exile_Entry,
OT_Mass_Add_Exile_Entry,
OT_Remove_Exile_Entry,
OT_Clear_Exile_List,
OT_Mass_Remove_Exile_Entry,
OT_Move_Exile_Entry_Up,
OT_Move_Exile_Entry_Down,
OT_Rename_Exile_Entry,


#parenting core
OT_Parent_The_Entry,
OT_Parent_Priority_Only,
OT_Parent_All_Entries,

#deparenting core
OT_Deparent_The_Entry,
OT_Deparent_Priority_Only,
OT_Deparent_All_Entries,


#main panel
PT_BasePanel,

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pine_tree = bpy.props.PointerProperty(type=ParentingTreeData)
    bpy.types.Scene.snip_snip = bpy.props.PointerProperty(type=DeparentingObjectData)
    bpy.types.Scene.extra = bpy.props.PointerProperty(type=AccessoryData)
  
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.pine_tree
    del bpy.types.Scene.snip_snip
    del bpy.types.Scene.extra
   
    
if __name__ == "__main__":

    register()
