import bpy
import bpy.ops
import os

class SpawnNames():

    #インデックス
    PROTOTYPE=0     # プロトタイプのオブジェクト名
    INSTANCE=1      # 量産時のオブジェクト名
    FILENAME=2      # リソースファイル名

    names = {}
    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["Player"]=("PrototypePlayerSpawn","PlayerSpawn","player/player.obj")
    names["Enemy"] = ("PrototypeEnemySpawn","EnemySpawn","enemy/enemy.obj")

#オペレータ 出現ポイントのシンボルを読み込む
class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description="出現ポイントのシンボルをImportします"

    def load_obj(self,type):
        print("出現ポイントのシンボルをImportします")

        # 重複ロード防止
        spawn_object=bpy.data.objects.get(SpawnNames.names[type][SpawnNames.PROTOTYPE])
        if spawn_object is not None:
            return {'CANCELLED'}

        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory=os.path.dirname(__file__)
        #ディレクトリからのモデルファイルの相対パスを記述
        releative_path=SpawnNames.names[type][SpawnNames.FILENAME]
        # 合成してモデルファイルのフルパスを得る
        full_path=os.path.join(addon_directory,releative_path)
        #オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',filepath=full_path,display_type='THUMBNAIL',forward_axis='Z',up_axis='Y')
        #回転を適用
        bpy.ops.object.transform_apply(location=False,rotation=True,scale=False,properties=False,isolate_users=False)
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name=SpawnNames.names[type][SpawnNames.PROTOTYPE]

        #オブジェクトの種類を設定
        object["type"]=SpawnNames.names[type][SpawnNames.INSTANCE]

        # メモリ上には置いておくがシーンから外す
        bpy.context.collection.objects.unlink(object)

        return {'FINISHED'}
    
    def execute(self,context):
        #Playerオブジェクト読み込み
        self.load_obj("Player")
        #Enemyオブジェクト読み込み
        self.load_obj("Enemy")

        return {'FINISHED'}
    
#オペレータ 出現ポイントのシンボルを作成・配置する
class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_spawn_create_symbol"
    bl_label="出現ポイントシンボルの作成"
    bl_description="出現ポイントのシンボルを作成します"
    bl_options={'REGISTER','UNDO'}

    # プロパティ（引数として渡せる）
    type: bpy.props.StringProperty(name="Type",default="Player")

    def execute(self,context):
        # コピー元オブジェクトを探す
        spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

        # まだ読み込んでいない場合は、インポート
        if spawn_object is None:
            bpy.ops.myaddon.myaddon_ot_spawn_import_symbol('EXEC_DEFAULT')
            spawn_object = bpy.data.objects.get(SpawnNames.names[self.type][SpawnNames.PROTOTYPE])

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
        new_object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        return {'FINISHED'}
        
#自キャラ専用出現ポイントシンボル作成オペレータ
class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label="プレイヤー出現ポイントシンボルの作成"
    bl_description="プレイヤー出現ポイントのシンボルを作成します"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):

        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Player")

        return {'FINISHED'}

#敵専用出現ポイントシンボル作成オペレータ
class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname="myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label="敵出現ポイントシンボルの作成"
    bl_description="敵出現ポイントのシンボルを作成します"
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):

        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol('EXEC_DEFAULT',type="Enemy")

        return {'FINISHED'}

