import bpy
from .properties import *

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


def register():
    bpy.utils.register_class(OT_Reveal_Object_Names)

def unregister():
    bpy.utils.unregister_class(OT_Reveal_Object_Names)

if __name__ == "__main__":
    register()