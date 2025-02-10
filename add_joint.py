import bpy
from bpy.props import StringProperty, FloatVectorProperty
import json
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, CollectionProperty
from bpy.types import PropertyGroup, Panel, Operator

# ジョイントのプロパティを定義
class JointProperty(bpy.types.PropertyGroup):
    id: StringProperty(
        name="ID",
        description="Unique ID for the joint",
        default=""
    )

    joint_type: bpy.props.EnumProperty(
        name="Joint Type",
        description="Type of the joint",
        items=[
            ('springJoint', "Spring Joint", "A spring-based joint"),
            ('pulleyJoint', "Pulley Joint", "A pulley-based joint"),
            ('unknown', "Unknown", "A custom joint type"),
        ],
        default='springJoint'
    )

    # Spring Joint properties
    springEnabled: FloatVectorProperty(
        name="Spring Enabled",
        description="Enable spring in XYZ directions",
        size=3,
        default=(1.0, 1.0, 1.0)
    )
    equilibriumPoint: FloatVectorProperty(
        name="Equilibrium Point",
        description="Equilibrium point of the spring",
        size=3,
        default=(0.0, 0.0, 0.0)
    )
    stiffness: FloatVectorProperty(
        name="Stiffness",
        description="Stiffness of the spring in XYZ directions",
        size=3,
        default=(10.0, 10.0, 10.0)
    )
    dampingCoefficient: FloatVectorProperty(
        name="Damping Coefficient",
        description="Damping coefficient for the spring",
        size=3,
        default=(0.5, 0.5, 0.5)
    )

    # Pulley Joint properties
    groundAnchor_A: FloatVectorProperty(
        name="Ground Anchor A",
        description="First ground anchor point for the pulley",
        size=3,
        default=(0.0, 0.0, 0.0)
    )
    groundAnchor_B: FloatVectorProperty(
        name="Ground Anchor B",
        description="Second ground anchor point for the pulley",
        size=3,
        default=(0.0, 0.0, 0.0)
    )
    anchor_A: FloatVectorProperty(
        name="Anchor A",
        description="First anchor point of the pulley",
        size=3,
        default=(1.0, 1.0, 1.0)
    )
    anchor_B: FloatVectorProperty(
        name="Anchor B",
        description="Second anchor point of the pulley",
        size=3,
        default=(1.0, 1.0, 1.0)
    )
    ratio: FloatVectorProperty(
        name="Ratio",
        description="Pulley ratio",
        size=1,
        default=(2.0,)
    )


# ジョイントの管理パネル
class SCENE_PT_ManageJoints(bpy.types.Panel):
    bl_label = "Manage Joints"
    bl_idname = "SCENE_PT_manage_joints"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # ジョイントをリストで表示
        row = layout.row()
        row.label(text="Joints in Scene:")

        for i, joint in enumerate(scene.joints):
            box = layout.box()
            row = box.row()
            row.prop(joint, "id", text=f"ID ")
            row.prop(joint, "joint_type", text=f"Joint {i+1}")
            
            # Spring JointとPulley Jointのパラメータを動的に表示
            if joint.joint_type == 'springJoint':
                row.prop(joint, "springEnabled")
                row.prop(joint, "equilibriumPoint")
                row.prop(joint, "stiffness")
                row.prop(joint, "dampingCoefficient")
            elif joint.joint_type == 'pulleyJoint':
                row.prop(joint, "groundAnchor_A", text="Ground Anchor A")
                row.prop(joint, "groundAnchor_B", text="Ground Anchor B")
                row.prop(joint, "anchor_A", text="Anchor A")
                row.prop(joint, "anchor_B", text="Anchor B")
                row.prop(joint, "ratio")

            # 削除ボタン
            row = box.row()
            row.operator("scene.delete_joint", text="Delete Joint").index = i

        # ジョイントを追加するボタン
        layout.operator("scene.add_joint", text="Add New Joint")
        # エクスポートボタン
        layout.operator("scene.export_joints", text="Export Joints to JSON")


# ジョイントを追加するオペレーター
class SCENE_OT_AddJoint(bpy.types.Operator):
    bl_idname = "scene.add_joint"
    bl_label = "Add New Joint"

    def execute(self, context):
        joint = context.scene.joints.add()
        joint.joint_type = 'springJoint'  # デフォルトのジョイントタイプ
        return {'FINISHED'}


# ジョイントを削除するオペレーター
class SCENE_OT_DeleteJoint(bpy.types.Operator):
    bl_idname = "scene.delete_joint"
    bl_label = "Delete Joint"

    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.joints.remove(self.index)
        return {'FINISHED'}


# ジョイントデータをエクスポートするオペレーター
class SCENE_OT_ExportJoints(bpy.types.Operator, ExportHelper):
    bl_idname = "scene.export_joints"
    bl_label = "Export Joints to JSON"
    
    filename_ext = ".json"
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        joints_data = []

        # ジョイントデータを収集
        for joint in context.scene.joints:
            joint_data = {
                "ID": joint.id,  # IDを追加
                "object_name": joint.name,  # オブジェクト名を動的に設定
                "type": joint.joint_type,
            }

            if joint.joint_type == 'springJoint':
                joint_data.update({
                    "springEnabled": list(joint.springEnabled),
                    "equilibriumPoint": list(joint.equilibriumPoint),
                    "stiffness": list(joint.stiffness),
                    "dampingCoefficient": list(joint.dampingCoefficient)
                })
            elif joint.joint_type == 'pulleyJoint':
                joint_data.update({
                    "groundAnchor": {
                        "A": list(joint.groundAnchor_A),
                        "B": list(joint.groundAnchor_B),
                    },
                    "anchor": {
                        "A": list(joint.anchor_A),
                        "B": list(joint.anchor_B),
                    },
                    "ratio": joint.ratio[0]
                })
            joints_data.append(joint_data)

        # エクスポート
        filepath = self.filepath
        with open(filepath, "w") as f:
            json.dump({"Joints": joints_data}, f, indent=4)

        self.report({'INFO'}, f"Joints exported to {filepath}")
        return {'FINISHED'}


# オブジェクトのIDを保持するプロパティ
class ObjectIDProperty(PropertyGroup):
    id: StringProperty(
        name="ID",
        description="Unique ID for the object",
        default=""
    )

# オブジェクトのIDを管理するパネル
class OBJECT_PT_ManageObjectIDs(Panel):
    bl_label = "Manage Object IDs"
    bl_idname = "OBJECT_PT_manage_object_ids"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # IDリストの表示
        row = layout.row()
        row.label(text="Object IDs:")
        
        if obj:
            for i, obj_id in enumerate(obj.object_ids):
                box = layout.box()
                row = box.row()
                row.prop(obj_id, "id", text=f"ID ")

                # 削除ボタン
                row = box.row()
                row.operator("object.delete_object_id", text="Delete ID").index = i

            # 新しいIDを追加するボタン
            row = layout.row()
            row.operator("object.add_object_id", text="Add New ID")


# オブジェクトにIDを追加するオペレーター
class OBJECT_OT_AddObjectID(Operator):
    bl_idname = "object.add_object_id"
    bl_label = "Add New Object ID"

    def execute(self, context):
        obj = context.object
        obj.object_ids.add()  # 新しいIDを追加
        return {'FINISHED'}


# オブジェクトからIDを削除するオペレーター
class OBJECT_OT_DeleteObjectID(Operator):
    bl_idname = "object.delete_object_id"
    bl_label = "Delete Object ID"

    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        obj.object_ids.remove(self.index)  # 指定されたインデックスのIDを削除
        return {'FINISHED'}