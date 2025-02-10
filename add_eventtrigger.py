import bpy

#オペレータ　カスタムプロパティ['EventTrigger']追加
class MYADDON_OT_add_eventtrigger(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_eventtrigger"
    bl_label = "イベントトリガー追加"
    bl_description = "['eventtrigger']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #['collider']カスタムプロパティを追加
        context.object["eventtrigger"] = int(0)
        return {"FINISHED"}


#パネル コライダー
class OBJECT_PT_eventtrigger(bpy.types.Panel):
    bl_idname = "OBJECT_PT_eventtrigger"
    bl_label = "EventTrigger"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニューの描画
    def draw(self, context):
        #パネルに項目を追加
        if "eventtrigger" in context.object:
            #既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object, '["eventtrigger"]', text="EventTrigger")
        else:
            #プロパティがなければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_eventtrigger.bl_idname)