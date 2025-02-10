import bpy

#オペレーター 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #redo、undo可能オプション
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行した時に呼ばれるコールバック関数
    def execute(self, context):
       bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
       print("頂点を伸ばしました。")

       #オペレーターの命令終了を通知
       return {'FINISHED'}