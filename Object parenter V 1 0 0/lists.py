import bpy

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
            row.prop(item, "child_priority")
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

classes = [
    
UL_Parent_History,
UL_Child_History,
UL_Object_History,
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()