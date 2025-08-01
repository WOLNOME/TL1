import bpy
import bpy_extras
import json
import math

# モジュールのインポート
from .load_objects import ObjectNames
from .load_objects import MYADDON_OT_load_objects

#オペレータ シーン読み込み
class MYADDON_OT_import_scene(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "myaddon.myaddon_ot_import_scene"
    bl_label = "シーン読み込み"
    bl_description = "シーン情報をImportします"
    bl_options={'REGISTER','UNDO'}
    #読み込むファイルの拡張子
    filename_ext = ".json"

    def execute(self,context):

        print("シーン情報をImportします")
        #ファイルに出力
        self.import_json()

        #出力終了通知
        print("シーン情報をImportしました")
        self.report({'INFO'},"シーン情報をimportしました")
        
        return {'FINISHED'}

    def import_json(self):
        """JSON形式のファイルを読み込み"""
        with open(self.filepath, "rt", encoding="utf-8") as file:
            json_text = file.read()

        json_data = json.loads(json_text)

        # ルートのオブジェクトリストを取得
        if "objects" in json_data:
            for obj_data in json_data["objects"]:
                self.create_object_recursive(obj_data, None)

    def create_object_recursive(self, data, parent):

        obj = None

        # typeによってモデルを読み込み＆複製
        obj_type = data.get("type", "")
        if obj_type in ObjectNames.names:
            prototype_name = ObjectNames.names[obj_type][ObjectNames.PROTOTYPE]
            instance_name = ObjectNames.names[obj_type][ObjectNames.INSTANCE]

            # プロトタイプが既に読み込まれているか確認
            prototype = bpy.data.objects.get(prototype_name)
            if prototype is None:
                # 存在しないならロード
                bpy.ops.myaddon.myaddon_ot_load_objects('EXEC_DEFAULT')
                prototype = bpy.data.objects.get(prototype_name)

            if prototype:
                # 複製してインスタンスとして使用
                obj = prototype.copy()
                obj.data = prototype.data.copy()
                bpy.context.collection.objects.link(obj)
                obj.name = data.get("name", instance_name)  # 名前をユニークにする
            else:
                self.report({'WARNING'}, f"{obj_type}のプロトタイプが見つかりません")
                return
        else:
            self.report({'WARNING'}, f"type '{obj_type}' が ObjectNames に存在しません")
            return

        obj.name = data.get("name")

        # transformの適用
        transform = data.get("transform", {})
        translation = transform.get("translation", [0, 0, 0])
        rotation = transform.get("rotation", [0, 0, 0])
        scaling = transform.get("scaling", [1, 1, 1])

        obj.location = translation
        obj.rotation_euler = [math.radians(x) for x in rotation]
        obj.scale = scaling

        # カスタムプロパティの読み込み
        if "type" in data:
            obj["type"] = data["type"]
        if "disabled" in data:
            obj["disabled"] = data["disabled"]
        if "file_name" in data:
            obj["file_name"] = data["file_name"]
        if "collider" in data:
            collider = data["collider"]
            obj["collider"] = collider.get("type", "")
            obj["collider_center"] = collider.get("center", [0, 0, 0])
            obj["collider_size"] = collider.get("size", [1, 1, 1])

        # 親がいる場合は階層を作る
        if parent:
            obj.parent = parent

        # 子供がいれば再帰的に作成
        for child_data in data.get("children", []):
            self.create_object_recursive(child_data, obj)