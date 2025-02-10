import bpy
import bpy_extras
import math
import json

#オペレーター　シーン出力
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExportします"
    #出力するファイルの拡張子
    filename_ext = ".json"

    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')

    def export(self):
        """ファイルに出力"""

        print("シーン情報出力開始... %r" % self.filepath)
        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath, "wt") as file:
            #ファイルに文字列を書き込む
            file.write("SCENE\n")
            
            #シーン内の全オブジェクトについて
            for object in bpy.context.scene.objects:

                #親オブジェクトがあるものはスキップ(代わりに親が呼び出すから)
                if(object.parent):
                    continue
                #シーン直下のオブジェクトをルートノード(深さ0)とし、再起関数で走査
                self.parse_scene_recursive(file, object, 0)

    def export_json(self):
        """JSON形式でファイルに出力"""

        #保存する情報をまとめるdict
        json_object_root = dict()

        #ノード名
        json_object_root["name"] = "scene"
        #オブジェクトリストを作成
        json_object_root["objects"] = list()

        #シーン内の全オブジェクトについて
        for object in bpy.context.scene.objects:
            #親オブジェクトがあるものはスキップ(代わりに親から呼び出すから)
            if(object.parent):
                continue

            #シーン直下のオブジェクトをルートノード(深さ0)とし、再起関数で走査
            self.parse_scene_recursive_json(json_object_root["objects"], object, 0)

        #オブジェクトをJSON文字列にエンコード(改行・インデント付き)
        json_text = json.dumps(json_object_root, ensure_ascii=False, cls=json.JSONEncoder, indent=4)

        #コンソールに表示してみる
        print(json_text)

        #ファイルをテキスト形式で書き出し用にオープン
        #スコープを抜けると自動的にクローズされる
        with open(self.filepath, "wt", encoding="utf-8") as file:

            #ファイルに文字列を書き込む
            file.write(json_text)

    def parse_scene_recursive_json(self, data_parent, object, level):

        #シーンのオブジェクト1個分のjsonオブジェクト生成
        json_object = dict()
        #オブジェクト種類
        json_object["type"] = object.type
        #オブジェクト名
        json_object["name"] = object.name

        #オブジェクトのローカルトランスフォームから
        #平行移動、回転、スケールを抽出
        trans, rot, scale = object.matrix_local.decompose()
        #回転をQuternionからEuler(3軸での回転角)に変換
        rot = rot.to_euler()
        #ラジアンから度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        #トランスフォーム情報をディクショナリに登録
        transform = dict()
        transform["translation"] = (trans.x, trans.y, trans.z)
        transform["rotation"] = (rot.x, rot.y, rot.z)
        transform["scaling"] = (scale.x, scale.y, scale.z)
        #まとめて1個分のjsonオブジェクトに登録
        json_object["transform"] = transform

        # オブジェクトが持つIDを登録
        if "object_ids" in object:
            json_object["jointIDs"] = [obj_id.id for obj_id in object.object_ids]

        #カスタムプロパティ '無効オプション'
        if "disabled" in object:
            json_object["disabled"] = object["disabled"]

        #カスタムプロパティ'file_name'
        if "file_name" in object:
            json_object["file_name"] = object["file_name"]

        #カスタムプロパティ'collider'
        if "collider" in object:
            collider = dict()
            collider["type"] = object["collider"]
            collider["center"] = object["collider_center"].to_list()
            collider["size"] = object["collider_size"].to_list()
            collider["isTrigger"] = object["collider_isTrigger"]
            collider["attribute"] = object["collider_attribute"]
            json_object["collider"] = collider
        
        #カスタムプロパティ'body'
        if "body" in object:
            body = dict()
            body["mass"] = object["body"]
            body["drag"] = object["body_drag"]
            body["miu"] = object["body_miu"]
            body["frictionCombine"] = object["body_frictionCombine"]
            body["bounciness"] = object["body_bounciness"]
            body["bounceCombine"] = object["body_bounceCombine"]
            json_object["body"] = body
        
        #カスタムプロパティ 'eventtrigger'
        if "eventtrigger" in object:
            eventtrigger = dict()
            eventtrigger["serialnumber"] = object["eventtrigger"]
            json_object["eventtrigger"] = eventtrigger

        #カスタムプロパティ 'tag'
        if "tag" in object:
            tag = dict()
            tag["tag"] = object["tag"]
            json_object["tag"] = tag
        
        #1個分のjsonオブジェクトを親オブジェクトに登録
        data_parent.append(json_object)

        #子ノードがあれば
        if len(object.children) > 0:
            #子ノードリストを作成
            json_object["children"] = list()

            #子ノードへ進む(深さが1上がる)
            for child in object.children:
                self.parse_scene_recursive_json(json_object["children"], child, level + 1)

            

    def execute(self, context):
        print("シーン情報をExportします")
        
        #ファイルに出力
        self.export_json()

        print("シーン情報をExportしました")
        self.report({'INFO'}, "シーン情報をExportしました")

        return {'FINISHED'}