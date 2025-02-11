import bpy
import math
import bpy_extras
import gpu
import gpu_extras.batch
import copy
import mathutils
import json
from bpy.props import CollectionProperty

# Blenderに登録するアドオン情報
bl_info = {
    "name": "レベルエディター",
    "author": "Maki Yukinori",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディター",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}

# モジュールのインポート
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .add_filename import MYADDON_OT_add_filename
from .add_filename import OBJECT_PT_file_name
from .add_collider import  MYADDON_OT_add_collider
from .add_collider import  OBJECT_PT_collider
from .draw_collider import DrawCollider
from .add_body import MYADDON_OT_add_body
from .add_body import OBJECT_PT_body
from .add_eventtrigger import MYADDON_OT_add_eventtrigger
from .add_eventtrigger import OBJECT_PT_eventtrigger
from .add_joint import JointProperty
from .add_joint import SCENE_PT_ManageJoints
from .add_joint import SCENE_OT_AddJoint
from .add_joint import SCENE_OT_DeleteJoint
from .add_joint import SCENE_OT_ExportJoints
from .add_joint import ObjectIDProperty
from .add_joint import OBJECT_PT_ManageObjectIDs
from .add_joint import OBJECT_OT_AddObjectID
from .add_joint import OBJECT_OT_DeleteObjectID
from .add_tag import MYADDON_OT_add_tag
from .add_tag import OBJECT_PT_tag
from .export_scene import MYADDON_OT_export_scene
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .disabled import MYADDON_OT_disabled
from .disabled import OBJECT_PT_disabled
from .spawn import MYADDON_OT_spawn_import_symbol
from .spawn import MYADDON_OT_spawn_create_symbol
from .spawn_player import MYADDON_OT_spawn_create_player_symbol
from .spawn_enemy import MYADDON_OT_spawn_create_enemy_symbol

#メニュー項目描画
def draw_menu_manual(self, context):
    #self : 呼び出し元のクラスインスタンス。C++でいうthisポインタ
    #context : カーソルを合わせた時のポップアップのカスタマイズなどに使用

    #トップバーの「エディターメニュー」に項目(オペレーター)を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon='HELP')

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #Blenderがクラスを識別する為の固有の文字列
    bl_idname = "TOPBAR_MT_my_menu"
    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by " + bl_info["author"]

    # サブメニューの描画
    def draw(self, context):

        #トップバーの「エディターメンテナンスメニュー」に項目(オペレーター)を追加
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label)
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text=MYADDON_OT_create_ico_sphere.bl_label)
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)
        self.layout.operator(MYADDON_OT_spawn_create_player_symbol.bl_idname, text=MYADDON_OT_spawn_create_player_symbol.bl_label)
        self.layout.operator(MYADDON_OT_spawn_create_enemy_symbol.bl_idname, text=MYADDON_OT_spawn_create_enemy_symbol.bl_label)
        self.layout.separator()
        # 区切り線
        self.layout.separator()
        # 区切り線
        self.layout.separator()
    
    # 既存のメニューにサブメニューを追加
    def submenu(self, context):

        # ID指定でサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname) 

# ジョイントの管理のためのプロパティを追加
def register_joint_properties():
    bpy.types.Scene.joints = bpy.props.CollectionProperty(type=JointProperty)

# オブジェクトにIDを追加するためのプロパティを登録
def register_object_id_properties():
    bpy.types.Object.object_ids = CollectionProperty(type=ObjectIDProperty)

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_export_scene,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_stretch_vertex,
    TOPBAR_MT_my_menu,
    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
    MYADDON_OT_add_body,
    OBJECT_PT_body,
    MYADDON_OT_add_eventtrigger,
    OBJECT_PT_eventtrigger,
    JointProperty,
    SCENE_PT_ManageJoints,
    SCENE_OT_AddJoint,
    SCENE_OT_DeleteJoint,
    SCENE_OT_ExportJoints,
    ObjectIDProperty,
    OBJECT_PT_ManageObjectIDs,
    OBJECT_OT_AddObjectID,
    OBJECT_OT_DeleteObjectID,
    MYADDON_OT_add_tag, 
    OBJECT_PT_tag,
    MYADDON_OT_disabled,
    OBJECT_PT_disabled,
    MYADDON_OT_spawn_import_symbol,
    MYADDON_OT_spawn_create_symbol,
    MYADDON_OT_spawn_create_player_symbol,
    MYADDON_OT_spawn_create_enemy_symbol
)

#Add-On有効化時コールバック
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")

    register_joint_properties()
    register_object_id_properties()
    print("レベルエディターが有効化されました。")


#Add-On無効化時コールバック
def unregister():
    #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle, "WINDOW")

    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.joints
    del bpy.types.Object.object_ids

    print("レベルエディターが無効化されました。")

if __name__ == "__main__":
    register()