import bpy
import math
import bpy_extras
import gpu
import gpu_extras.batch
import copy
import mathutils
import json

# ブレンダーに登録するアドオン情報
bl_info = {
    "name": "レベルエディタ",
    "author": "Yuki Ushio",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# モジュールのインポート
from .create_ico_sphere import MYADDON_OT_create_ico_sphere
from .stretch_vertex import MYADDON_OT_stretch_vertex
from .export_scene import MYADDON_OT_export_scene
from .my_menu import TOPBAR_MT_my_menu
from .add_filename import MYADDON_OT_add_filename
from .file_name import OBJECT_PT_file_name
from .add_collider import MYADDON_OT_add_collider
from .collider import OBJECT_PT_collider
from .collider import DrawCollider

# アドオン有効時の初期コールバック
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    #メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)

    #3Dビューに描画関数を追加
    DrawCollider.handle=bpy.types.SpaceView3D.draw_handler_add(DrawCollider.draw_collider,(),"WINDOW","POST_VIEW")

    print("レベルエディタが有効化されました。")

# アドオン無効化時のコールバック
def unregister():
    #メニューから項目を削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)

    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(DrawCollider.handle,"WINDOW")

    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタが無効化されました。")

# テスト実行用コード
if __name__ == "__main__":
    register()

#Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_export_scene,

    TOPBAR_MT_my_menu,

    MYADDON_OT_add_filename,
    OBJECT_PT_file_name,
    MYADDON_OT_add_collider,
    OBJECT_PT_collider,
)
