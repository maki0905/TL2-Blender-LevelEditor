import bpy

#オペレータ　カスタムプロパティ Body
class MYADDON_OT_add_body(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_body"
    bl_label = "ボディー追加"
    bl_description = "['body']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        obj["body"] = float(0.0)
        obj["body_drag"] = float(0.05)
        obj["body_miu"] = float(0.0)
        obj["body_frictionCombine"] = int(0)
        obj["body_bounciness"] = float(0.0)
        obj["body_bounceCombine"] = int(0)
        return {"FINISHED"}


#パネル Body
class OBJECT_PT_body(bpy.types.Panel):
    bl_idname = "OBJECT_PT_body"
    bl_label = "Body"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if "body" in obj:
            layout.prop(obj, '["body"]', text="Mass")
            layout.prop(obj, '["body_drag"]', text="Air Resistance")
            layout.prop(obj, '["body_miu"]', text="Miu")
            layout.prop(obj, '["body_frictionCombine"]', text="Friction Combine")
            layout.prop(obj, '["body_bounciness"]', text="Bounciness")
            layout.prop(obj, '["body_bounceCombine"]', text="Bounce Combine")
        else:
            layout.operator(MYADDON_OT_add_body.bl_idname)