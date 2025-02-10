import bpy

#オペレータ　カスタムプロパティ['Tag']追加
class MYADDON_OT_add_tag(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_tag"
    bl_label = "タグ追加"
    bl_description = "['tag']カスタムプロパティを追加します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #['collider']カスタムプロパティを追加
        context.object["tag"] = int(0)
        return {"FINISHED"}


#パネル ジョイント
class OBJECT_PT_tag(bpy.types.Panel):
    bl_idname = "OBJECT_PT_tag"
    bl_label = "Tag"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    #サブメニューの描画
    def draw(self, context):
        #パネルに項目を追加
        if "tag" in context.object:
            #既にプロパティがあれば、プロパティを表示
            self.layout.prop(context.object, '["tag"]', text="Tag")
        else:
            #プロパティがなければ、プロパティ追加ボタンを表示
            self.layout.operator(MYADDON_OT_add_tag.bl_idname)