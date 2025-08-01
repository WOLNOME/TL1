import bpy
import bpy.ops
import os

class ObjectNames():

    #インデックス
    PROTOTYPE=0     # プロトタイプのオブジェクト名
    INSTANCE=1      # 量産時のオブジェクト名
    FILENAME=2      # リソースファイル名

    names = {}
    # names["キー"] = (プロトタイプのオブジェクト名、量産時のオブジェクト名、リソースファイル名)
    names["PlayerSpawn"]=("PrototypePlayerSpawn","PlayerSpawn","player/player.obj")
    names["EnemySpawn"] = ("PrototypeEnemySpawn","EnemySpawn","enemy/enemy.obj")
    names["TreeObject"]=("PrototypeTreeObject","TreeObject","tree/tree.obj")

#オペレータ オブジェクトをロードする
class MYADDON_OT_load_objects(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_load_objects"
    bl_label = "オブジェクトLoad"
    bl_description="オブジェクトをLoadします"

    def load_obj(self,type):
        print("オブジェクトをLoadします")

        # 重複ロード防止
        load_object=bpy.data.objects.get(ObjectNames.names[type][ObjectNames.PROTOTYPE])
        if load_object is not None:
            return {'CANCELLED'}

        # スクリプトが配置されているディレクトリの名前を取得する
        addon_directory=os.path.dirname(__file__)
        #ディレクトリからのモデルファイルの相対パスを記述
        releative_path=ObjectNames.names[type][ObjectNames.FILENAME]
        # 合成してモデルファイルのフルパスを得る
        full_path=os.path.join(addon_directory,releative_path)
        #オブジェクトをインポート
        bpy.ops.wm.obj_import('EXEC_DEFAULT',filepath=full_path,display_type='THUMBNAIL',forward_axis='Z',up_axis='Y')
        #回転を適用
        bpy.ops.object.transform_apply(location=False,rotation=True,scale=False,properties=False,isolate_users=False)
        # アクティブなオブジェクトを取得
        object = bpy.context.active_object
        # オブジェクト名を変更
        object.name=ObjectNames.names[type][ObjectNames.PROTOTYPE]

        #オブジェクトの種類を設定
        object["type"]=ObjectNames.names[type][ObjectNames.INSTANCE]

        # メモリ上には置いておくがシーンから外す
        bpy.context.collection.objects.unlink(object)

        return {'FINISHED'}
    
    def execute(self,context):
        #Playerオブジェクト読み込み
        self.load_obj("PlayerSpawn")
        #Enemyオブジェクト読み込み
        self.load_obj("EnemySpawn")
        #Treeオブジェクト読み込み
        self.load_obj("TreeObject")

        return {'FINISHED'}
    