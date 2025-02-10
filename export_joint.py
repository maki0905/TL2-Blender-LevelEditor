import bpy
import json
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

# ジョイントのプロパティを定義
class JointProperty(bpy.types.PropertyGroup):
    joint_type: bpy.props.EnumProperty(
        name="Joint Type",
        description="Type of the joint",
        items=[
            ('springJoint', "Spring Joint", "A spring-based joint"),
            ('pulleyJoint', "Pulley Joint", "A pulley-based joint"),
        ],
        default='springJoint'
    )

    # Spring Joint properties
    springEnabled: bpy.props.FloatVectorProperty(
        name="Spring Enabled",
        description="Enable spring in XYZ directions",
        size=3,
        default=(1.0, 1.0, 1.0)
    )
    equilibriumPoint: bpy.props.FloatVectorProperty(
        name="Equilibrium Point",
        description="Equilibrium point of the spring",
        size=3,
        default=(0.0, 0.0, 0.0)
    )
    stiffness: bpy.props.FloatVectorProperty(
        name="Stiffness",
        description="Stiffness of the spring in XYZ directions",
        size=3,
        default=(10.0, 10.0, 10.0)
    )
    dampingCoefficient: bpy.props.FloatVectorProperty(
        name="Damping Coefficient",
        description="Damping coefficient for the spring",
        size=3,
        default=(0.5, 0.5, 0.5)
    )

    # Pulley Joint properties
    groundAnchor: bpy.props.FloatVectorProperty(
        name="Ground Anchor",
        description="Ground anchor point for the pulley",
        size=3,
        default=(0.0, 0.0, 0.0)
    )
    anchor: bpy.props.FloatVectorProperty(
        name="Anchor",
        description="Anchor point of the pulley",
        size=3,
        default=(1.0, 1.0, 1.0)
    )
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Pulley ratio",
        default=2.0
    )

    # カスタムプロパティ（unknown joint用）
    custom_property_1: bpy.props.StringProperty(
        name="Custom Property 1",
        description="A custom property for unknown joints",
        default="value1"
    )
    custom_property_2: bpy.props.StringProperty(
        name="Custom Property 2",
        description="Another custom property for unknown joints",
        default="value2"
    )


# シーンプロパティパネルにエクスポート機能を追加
class SCENE_PT_ExportJoints(bpy.types.Panel):
    bl_label = "Export Joints"
    bl_idname = "SCENE_PT_export_joints"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        # エクスポートボタンを追加
        layout.operator("scene.export_all_joints", text="Export All Joints")


# ジョイントをエクスポートするオペレーター
class SCENE_OT_ExportAllJoints(bpy.types.Operator, ImportHelper):
    bl_idname = "scene.export_all_joints"
    bl_label = "Export All Joints"
    bl_description = "Export all joint data from the scene to a JSON file"

    # ファイルパスを格納するプロパティ
    filename_ext = ".json"
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'}
    )

    def execute(self, context):
        joints_data = []

        # シーン内のすべてのオブジェクトを確認
        for obj in bpy.context.scene.objects:
            if hasattr(obj, "joints"):  # オブジェクトにジョイントがあるか確認
                for joint in obj.joints:
                    joint_data = {
                        "object_name": obj.name,
                        "type": joint.joint_type,  # ジョイントタイプを保存
                    }

                    # ジョイントの種類ごとに異なるプロパティを追加
                    if joint.joint_type == 'springJoint':
                        joint_data.update({
                            "springEnabled": list(joint.springEnabled),
                            "equilibriumPoint": list(joint.equilibriumPoint),
                            "stiffness": list(joint.stiffness),
                            "dampingCoefficient": list(joint.dampingCoefficient)
                        })
                    elif joint.joint_type == 'pulleyJoint':
                        joint_data.update({
                            "groundAnchor": list(joint.groundAnchor),
                            "anchor": list(joint.anchor),
                            "ratio": joint.ratio
                        })
                    else:
                        # 未知のジョイントタイプの場合、カスタムプロパティを追加
                        joint_data["properties"] = {
                            "custom_property_1": joint.custom_property_1,
                            "custom_property_2": joint.custom_property_2
                        }

                    joints_data.append(joint_data)

        # エクスポートするファイルパスを取得
        filepath = self.filepath

        # JSON形式でデータを保存
        with open(filepath, "w") as f:
            json.dump({"Joints": joints_data}, f, indent=4)

        self.report({'INFO'}, f"Joints exported to {filepath}")
        return {'FINISHED'}


# ジョイントを管理するコレクションプロパティをオブジェクトに追加
def register_joint_properties():
    bpy.types.Object.joints = bpy.props.CollectionProperty(type=JointProperty)


# 登録と解除
classes = [
    JointProperty,
    SCENE_PT_ExportJoints,
    SCENE_OT_ExportAllJoints,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_joint_properties()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.joints

if __name__ == "__main__":
    register()
