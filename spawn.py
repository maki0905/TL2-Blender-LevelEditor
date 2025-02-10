import bpy
import os
import bpy.ops

#オペレーター 頂点を伸ばす
class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをImportします"
    prottype_object_name = "ProttypePlayerSpawn"
    object_name = "PlayerSpawn"
    #redo、undo可能オプション
    bl_options = {'REGISTER', 'UNDO'}

    #メニューを実行した時に呼ばれるコールバック関数
    def execute(self, context):
       print("出現ポイントのシンボルをImportします")
       # スクリプトが配置されているディレクトリの名前を取得
       addon_directory = os.path.dirname(__file__)
       # ディレクトリからのモデルファイルの相対パスを記述
       relative_path = "player/player.obj"
       # 合成してモデルファイルのフルパスを得る
       full_path = os.path.join(addon_directory, relative_path)
       # オブジェクトをインポート
       bpy.ops.wm.obj_import('EXEC_DEFAULT', filepath = full_path, display_type='THUMBNAIL', forward_axis='Z', up_axis='Y')
       # 回転の適用
       bpy.ops.object.transform_apply(location=False, rotation=True, scale=False, properties=False, isolate_users=False)
       # アクティブなオブジェクトを取得
       object = bpy.context.active_object
       #オブジェクト名を変更
       object.name = MYADDON_OT_spawn_import_symbol.prottype_object_name
       # オブジェクトの種類を設定
       object["type"] = MYADDON_OT_spawn_import_symbol.object_name
       #オペレーターの命令終了を通知
       return {'FINISHED'}