import bpy
import mathutils
import math
import gpu
import gpu_extras.batch

#コライダー描画
class DrawCollider:

    #描画ハンドル
    handle = None

    #Sphereの頂点を生成
    def create_sphere_vertices(radius=1.0, segments=16, rings=8):
        vertices = []
        indices = []

        gpu.state.depth_test_set("LESS")

        for i in range(rings + 1):
            theta = i * math.pi / rings
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for j in range(segments):
                phi = j * 2 * math.pi / segments
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                x = cos_phi * sin_theta
                y = sin_phi * sin_theta
                z = cos_theta

                vertices.append((radius * x, radius * y, radius * z))

        for i in range(rings):
            for j in range(segments):
                first = (i * segments) + j
                second = first + segments

                indices.append((first, second))
                indices.append((first, first + 1 if (j + 1) % segments else first + 1 - segments))
                indices.append((second, second + 1 if (j + 1) % segments else second + 1 - segments))

        return vertices, indices
    
    #Boxの頂点を生成
    def create_box_vertices(size):
        offsets = [
            [-0.5, -0.5, -0.5], #左下前
            [+0.5, -0.5, -0.5], #右下前
            [-0.5, +0.5, -0.5], #左上前
            [+0.5, +0.5, -0.5], #右上前
            [-0.5, -0.5, +0.5], #左下奥
            [+0.5, -0.5, +0.5], #右下奥
            [-0.5, +0.5, +0.5], #左上奥
            [+0.5, +0.5, +0.5], #右上奥
        ]
        
        vertices = []
        indices = []

        gpu.state.depth_test_set("LESS")

        for offset in offsets:
            vertices.append((
                offset[0] * size[0],
                offset[1] * size[1],
                offset[2] * size[2]
            ))

        indices.extend([
            (0, 1), (2, 3), (0, 2), (1, 3),  # 前面
            (4, 5), (6, 7), (4, 6), (5, 7),  # 奥面
            (0, 4), (1, 5), (2, 6), (3, 7)   # 前と奥を繋ぐ辺
        ])

        return vertices, indices

    #3Dビューに登録する描画関数
    def draw_collider():
        #頂点データ
        vertices = {"pos":[]}
        #インデックスデータ
        indices = []

        #各頂点の、オブジェクト中心からのオフセット
        offsets = [
            [-0.5, -0.5, -0.5], #左下前
            [+0.5, -0.5, -0.5], #右下前
            [-0.5, +0.5, -0.5], #左上前
            [+0.5, +0.5, -0.5], #右上前
            [-0.5, -0.5, +0.5], #左下奥
            [+0.5, -0.5, +0.5], #右下奥
            [-0.5, +0.5, +0.5], #左上奥
            [+0.5, +0.5, +0.5], #右上奥
        ]

        #立方体のX, Y, Z方向サイズ
        size = [2,2,2]

        #現在シーンのオブジェクトリストを走査
        for object in bpy.context.scene.objects:

            #コライダープロパティがなければ、描画をスキップ
            if not "collider" in object:
                continue

            #中心点、サイズの変数を宣言
            center = mathutils.Vector((0, 0, 0))
            size = mathutils.Vector((2, 2, 2))

            #プロパティから値を取得
            center[0] = object["collider_center"][0]
            center[1] = object["collider_center"][1]
            center[2] = object["collider_center"][2]
            size[0] = object["collider_size"][0]
            size[1] = object["collider_size"][1]
            size[2] = object["collider_size"][2]

            # 描画するコライダーの種類を判定
            collider_type = object["collider"]

            # 頂点とエッジを作成
            if collider_type == "SPHERE":
                shape_vertices, shape_indices = DrawCollider.create_sphere_vertices(radius=size[0])
            else:  # "box" またはその他
                shape_vertices, shape_indices = DrawCollider.create_box_vertices(size)

            # 頂点をワールド座標に変換して追加
            start = len(vertices["pos"])
            for vert in shape_vertices:
                pos = mathutils.Vector(vert) + center
                pos = object.matrix_world @ pos
                vertices['pos'].append(pos)

            # インデックスを追加
            for edge in shape_indices:
                indices.append((start + edge[0], start + edge[1]))

        gpu.state.depth_test_set("LESS")    
        #ビルトインのシェーダを取得
        shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

        # バッチを作成(引数:シェーダ、トポロジー、頂点データ、インデックスデータ)
        batch = gpu_extras.batch.batch_for_shader(shader, "LINES", vertices, indices = indices)

        #シェーダのパラメータ設定
        color = [0.5, 1.0, 1.0, 1.0]
        shader.bind()
        shader.uniform_float("color", color)
        # 描画
        batch.draw(shader)