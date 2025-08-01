import bpy
import bpy.ops

# モジュールのインポート
from .load_objects import ObjectNames
from .load_objects import MYADDON_OT_load_objects

#オペレータ 出現ポイントのシンボルを作成・配置する
class MYADDON_OT_create_object(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_create_object"
    bl_label="オブジェクトの作成"
    bl_description="オブジェクトを作成します"
    bl_options={'REGISTER','UNDO'}

    # プロパティ（引数として渡せる）
    type: bpy.props.StringProperty(name="Type",default="PlayerSpawn")

    def execute(self,context):
        # コピー元オブジェクトを探す
        spawn_object = bpy.data.objects.get(ObjectNames.names[self.type][ObjectNames.PROTOTYPE])
        
        # まだ読み込んでいない場合は、インポート
        if spawn_object is None:
            bpy.ops.myaddon.myaddon_ot_load_objects('EXEC_DEFAULT')
            spawn_object = bpy.data.objects.get(ObjectNames.names[self.type][ObjectNames.PROTOTYPE])

            if spawn_object is None:
                self.report({'ERROR'}, f"{self.type} のスプローンオブジェクトが見つかりません")
                return {'CANCELLED'}

        print("出現ポイントのシンボルを作成します")

        # 選択解除
        bpy.ops.object.select_all(action='DESELECT')

        # 複製
        new_object = spawn_object.copy()

        # シーンにリンク
        bpy.context.collection.objects.link(new_object)

        # オブジェクト名を変更
        new_object.name = ObjectNames.names[self.type][ObjectNames.INSTANCE]

        return {'FINISHED'}
        
#自キャラ専用出現ポイントシンボル作成オペレータ
class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label="プレイヤー出現ポイントシンボルの作成"
    bl_description="プレイヤー出現ポイントのシンボルを作成します"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):

        bpy.ops.myaddon.myaddon_ot_create_object('EXEC_DEFAULT',type="PlayerSpawn")

        return {'FINISHED'}

#敵専用出現ポイントシンボル作成オペレータ
class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label="敵出現ポイントシンボルの作成"
    bl_description="敵出現ポイントのシンボルを作成します"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):

        bpy.ops.myaddon.myaddon_ot_create_object('EXEC_DEFAULT',type="EnemySpawn")

        return {'FINISHED'}
    
#ツリーオブジェクト作成オペレータ
class MYADDON_OT_create_tree_object(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_create_tree_object"
    bl_label="ツリーオブジェクトの作成"
    bl_description="ツリーオブジェクトを作成します"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):

        bpy.ops.myaddon.myaddon_ot_create_object('EXEC_DEFAULT',type="TreeObject")

        return {'FINISHED'}


