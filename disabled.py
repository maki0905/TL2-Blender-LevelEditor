import bpy

#オペレータ　カスタムプロパティ Disabled
class MYADDON_OT_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_disabled"
    bl_label = "無効フラグ追加"
    bl_description = "['disabled']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        obj["disabled"] = True
        
        return {"FINISHED"}


#パネル Disabled
class OBJECT_PT_disabled(bpy.types.Panel):
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "Disabled"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if "disabled" in obj:
            layout.prop(obj, '["disabled"]', text="Flag")
        else:
            layout.operator(MYADDON_OT_disabled.bl_idname)