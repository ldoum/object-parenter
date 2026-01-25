### 1129pm 1/23/2026 Friday - made this for starlight project

import bpy

bl_info = {
    "name": "Object Parenter Chain", 
    "blender": (2, 8, 0),
    "category": "Object",
    "author": "Lancine Doumbia", 
    "version": (0, 1, 0), 
    "location": "View3D > Sidebar", #important
    "description": "Automate the process of parenting in a chain. First to last", 
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
}


####  core functionality  ####    
def assign_children_to_parent(parent_name, child_name):
    
    #access this object 
    parent_ = bpy.context.scene.objects.get(parent_name)
         
    #if child list isnt empty and the parent object exists
    if child_name and parent_:   
                                                        
        child_ = bpy.context.scene.objects.get(child_name) #get child
             
        #if child exists:
        if child_: 
                     
            #parent this object                     
            child_.parent = parent_   
            
            #keep transform                                      
            child_.matrix_parent_inverse = parent_.matrix_world.inverted()  

    

### helper function - makw object active
def make_parent_object_active(self, context):
    
    pine_ = context.scene.pine_
       
    #get parent entry name
    parent_name = pine_.parents_list[pine_.parent_idx].parent_name
    
    #get if object exists
    obj = context.scene.objects.get(parent_name)

    if obj:
        # Deselect all other objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        #select the object
        obj.select_set(True)
        #make it active
        context.view_layer.objects.active = obj


#duplicate entry guards. flips through history of the list, stop loop if the match is found    
def parent_entry_exists(collection, obj_name):
    for item in collection:                   
        if item.parent_name == obj_name:      
            return True
    return False                          



class ParentObjectEntryXX(bpy.types.PropertyGroup):
    parent_name: bpy.props.StringProperty(name="Parent Name")
    parent_type: bpy.props.StringProperty(name="Parent Type")
    parent_priority: bpy.props.BoolProperty(name="Priority", default=False)
    
class ParentingTreeDataXX(bpy.types.PropertyGroup):    
    parents_list: bpy.props.CollectionProperty(type=ParentObjectEntryXX)
    parent_idx: bpy.props.IntProperty(
                name="Active Index for Parent", 
                default=0,
                update=make_parent_object_active,
                )
    parent_rename: bpy.props.StringProperty(
                    name="New Parent Name",
                    )
    show_names: bpy.props.BoolProperty(
                    name="Show names?",
                    default=False,
                    )  
    
    
class UL_Parent_HistoryXX(bpy.types.UIList):
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



class OT_Add_Parent_EntryXX(bpy.types.Operator):
    bl_idname = "operator.add_parent_entry_"
    bl_label = "Add Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
        obj = context.active_object
       
        #guard method to prevent duplicate entries
        if not parent_entry_exists(pine_.parents_list, obj.name):
            #add new entry
            new_entry = pine_.parents_list.add() 
            #insert object data
            new_entry.parent_name = obj.name
            new_entry.parent_type = obj.type
            #place new entry via index
            pine_.parent_idx = len(pine_.parents_list)-1

            return {"FINISHED"}
        else:
            self.report({'INFO'}, "The item already exists")
            return {"CANCELLED"}



class OT_Remove_Parent_EntryXX(bpy.types.Operator):
    bl_idname = "operator.remove_parent_entry_"
    bl_label = "Remove Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_ = context.scene.pine_
        return True if len(pine_.parents_list) > 0 else False

    def execute(self, context):
        pine_ = context.scene.pine_
        
        #remove entry by indice
        pine_.parents_list.remove(pine_.parent_idx)
        
        #make index point to next entry 
        pine_.parent_idx = min(pine_.parent_idx, len(pine_.parents_list)-1)

        return {"FINISHED"}



class OT_Clear_Parent_ListXX(bpy.types.Operator):
    bl_idname = "operator.clear_parent_list_"
    bl_label = "Clear Parent List"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_ = context.scene.pine_ 
        return True if pine_.parents_list else False

    def execute(self, context):
        pine_ = context.scene.pine_
        #clear list
        pine_.parents_list.clear() 
        #reset index
        pine_.parent_idx = 0

        return {"FINISHED"}


#### mass subtract op
class OT_Mass_Remove_Parent_EntryXX(bpy.types.Operator):
    bl_idname = "operator.mass_remove_parent_entry_"
    bl_label = "Remove More Parent Entries"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    #if list is empty, disable
    @classmethod
    def poll(cls,context):
        pine_ = context.scene.pine_
        return True if len(pine_.parents_list) > 0 else False

    def execute(self, context):
        pine_ = context.scene.pine_
        
        #loop backwards to avoid index shifting issues
        for idx in reversed(range(len(pine_.parents_list))):
            
            #get entry by indice
            base_obj = pine_.parents_list[idx]
            
            #check if object priority checkbox is clicked
            if base_obj.parent_priority == True:
            
                #remove this entry as its no longer needed
                pine_.parents_list.remove(idx)
    
                #make index point to next entry 
                pine_.parent_idx = min(idx, len(pine_.parents_list)-1)
        
        ###########################
        
                
        return {"FINISHED"}     
    
class OT_Move_Parent_Entry_UpXX(bpy.types.Operator):
    bl_idname = "operator.move_parent_entry_up_"
    bl_label = "Ascend Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
        
        #move entry up to indice A - 1. above
        pine_.parent_list.move(pine_.parent_idx, self.parent_idx - 1) 
        
        #make list point to moved entry
        pine_.parent_idx = max(0, pine_.parent_idx - 1)
        
        return {"FINISHED"}
        
        
class OT_Move_Parent_Entry_DownXX(bpy.types.Operator):
    bl_idname = "operator.move_parent_entry_down_"
    bl_label = "Descend Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
        
        #move entry down to indice A + 1. above
        pine_.parent_list.move(pine_.parent_idx, pine_.parent_idx + 1) 
        
        #make list point to moved entry
        pine_.parent_idx = min(pine_.parent_idx + 1, len(pine_.parents_list) - 1)

        return {"FINISHED"}
    
### rename op here    

class OT_Rename_Parent_EntryXX(bpy.types.Operator):
    bl_idname = "operator.rename_parent_entry_"
    bl_label = "Rename Parent Entry"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
        
        #get parent entry name
        parent_name = pine_.parents_list[pine_.parent_idx].parent_name
    
        #access existing object in the active scene
        obj = context.scene.objects[parent_name]
        #rename
        obj.name = pine_.parent_rename 
        #edit active entry name
        pine_.parents_list[pine_.parent_idx].parent_name = pine_.parent_rename
        
        return {"FINISHED"}


class OT_Reveal_Object_NamesXX(bpy.types.Operator):
    bl_idname = "operator.reveal_names_"
    bl_label = "Reveal Object Names"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
   
        #apply
        for each_obj in context.selected_objects:
            
            if pine_.show_names == True:
                each_obj.show_name = pine_.show_names
            else:
                each_obj.show_name = pine_.show_names
       
        return {"FINISHED"}


class OT_Parent_Entry_ChainXX(bpy.types.Operator):
    bl_idname = "operator.parent_chain_"
    bl_label = "Parent These Objects"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    
    def execute(self, context):
        pine_ = context.scene.pine_
        
        
        #go through each parent in main list
        #main_obj acts like pine_tree.parents_list[pine_tree.parent_idx]
        for m in range(len(pine_.parents_list)-1):
            
            one = pine_.parents_list[m].parent_name
            two = pine_.parents_list[m+1].parent_name
            
            #call this method for each parent object   
            assign_children_to_parent(one, two)
            
        #finally, clear the entire parent list
        pine_.parents_list.clear()
  
        return {"FINISHED"}


class PT_BasePanelXX(bpy.types.Panel):
    bl_idname = "panel.parent_chain"
    bl_label = "Parent Chain"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Parenter"
    
    #show up in object mode only
    @classmethod
    def poll(cls,context):
        return context.mode == "OBJECT"

    def draw(self, context):
        layout = self.layout
        assign_ = context.scene.pine_
        
        ### accessory panel
        box = layout.box().row()
        box.prop(assign_, "show_names")
        box.operator(OT_Reveal_Object_NamesXX.bl_idname, text="Apply")
        
        #parent window
        layout.label(text="Parenting")
        
        #parent list
        layout.template_list(
            "UL_Parent_HistoryXX", "", #List class name, list id
            assign_, "parents_list", # Collection property
            assign_, "parent_idx", # Active property
        )
            
            
        #parent object rename
        row = layout.row(align=True)
        row.prop(assign_, "parent_rename")
        row.operator(OT_Rename_Parent_EntryXX.bl_idname, text="", icon="CHECKMARK")
         
        #manage parent list
        row = layout.row(align=True)
        row.operator(OT_Add_Parent_EntryXX.bl_idname, text="+")
        row.operator(OT_Remove_Parent_EntryXX.bl_idname, text="-")
        row.operator(OT_Mass_Remove_Parent_EntryXX.bl_idname, text="--")
        row.operator(OT_Clear_Parent_ListXX.bl_idname, text="", icon="TRASH")
        row.operator(OT_Move_Parent_Entry_UpXX.bl_idname, text="", icon="TRIA_UP")
        row.operator(OT_Move_Parent_Entry_DownXX.bl_idname, text="", icon="TRIA_DOWN")
        
        
        
        #if parents list has something
        if assign_.parents_list:
                
            #access child subentry
            parent_active = assign_.parents_list[assign_.parent_idx]
                
            #retrieve name of active parent obj and access it
            main_obj = context.scene.objects.get(parent_active.parent_name)
                
            #check if object exists to avoid key errors for bpy_prop_collection
            if main_obj:

                #if it has a parent, display the box
                if main_obj.parent:
                    layout.label(text=f"Parent of {parent_active.parent_name}: {main_obj.parent.name} ")
                 
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
              
                
        row = layout.row()
        row.operator(OT_Parent_Entry_ChainXX.bl_idname, text="Parent All")
        

classes = [
    ParentObjectEntryXX,
    ParentingTreeDataXX,
    UL_Parent_HistoryXX,
    
    OT_Add_Parent_EntryXX,
    OT_Remove_Parent_EntryXX,
    OT_Clear_Parent_ListXX,
    OT_Mass_Remove_Parent_EntryXX,
    OT_Move_Parent_Entry_UpXX,
    OT_Move_Parent_Entry_DownXX,
    OT_Rename_Parent_EntryXX,

    

    OT_Reveal_Object_NamesXX,

    OT_Parent_Entry_ChainXX,
    PT_BasePanelXX,

]    
    

    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pine_ = bpy.props.PointerProperty(type=ParentingTreeDataXX)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.pine_
    
if __name__ == "__main__":
    register()
