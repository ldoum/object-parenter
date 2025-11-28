import bpy
from .properties import *
from .parenting_operators import *
from .parent_list_operators import *    
from .deparenting_operators import *
from .deparent_list_operators import *  
from .reveal_object_names_operator import OT_Reveal_Object_Names
from .child_list_operators import *
from .lists import *

class PT_BasePanel(bpy.types.Panel):
    bl_idname = "panel.parent_deparent_define"
    bl_label = "List panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    
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


def register():
    bpy.utils.register_class(PT_BasePanel)

def unregister():
    bpy.utils.unregister_class(PT_BasePanel)

if __name__ == "__main__":

    register()

