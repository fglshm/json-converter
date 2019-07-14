import sys
import json
import os
import re
from enum import Enum


def check_type(val):
    '''
        値の型をチェックする関数
    '''
    if type(val) == int:
        if len(str(val)) > 8:
            return 'Long'
        else:
            return 'Int'
    elif type(val) == str:
        return 'String'
    elif type(val) == bool:
        return 'Boolean'
    else:
        return 'Any'


def convert(key, option):
    """
        key にアンダースコアが含まれなくなるまでループを回す
    """

    # return 用の key
    new_key = key

    # remove_underscore に渡す用の key
    tmp_key = key

    while True:
        if not '_' in new_key:
            if option:
                return add_m_head(new_key)
            else:
                return new_key

        tmp_key = remove_underscore(tmp_key)
        new_key = tmp_key


def remove_underscore(key):
    # アンダースコアの位置
    us_idx = key.index('_')

    # keyをリストに変換
    key_char_list = list(key)

    # アンダースコアを削除
    del key_char_list[us_idx]

    # アンダースコアの次の文字を大文字に置換
    # アンダースコア削除後は、us_idx は元の key のアンダースコアの次の文字のインデックスになる
    key_char_list[us_idx] = key_char_list[us_idx].upper()

    # リストの文字を連結させて返す
    return ''.join(key_char_list)


def add_anotation(old, new, t):
    """
        Kotlin のクラスのメンバ変数定義のように文字列を生成
        --------------------------
        @SerializedName(user_id)
        var userId: String? = null
        --------------------------
    """
    ant = '@SerializedName("%s")' % old
    var_decl = 'var %s: %s? = null' % (new, t)
    return [ant, var_decl]


def add_m_head(key):
    lst = list(key)
    lst[0] = lst[0].upper()
    return 'm' + ''.join(lst)


args = sys.argv
len_args = len(args)

if len_args is 1:
    print('変換する JSON ファイルを入力してください.')
    sys.exit()
elif len_args is 2:
    print('変換後のファイル名を入力してください.')
    sys.exit()
elif len_args is 3:
    print('変換を開始します.')
elif len_args is 4:
    print('オプション m　を追加してください.')
    sys.exit()
elif len_args is 5:
    print('変換を開始します.')
else:
    print('正しいコマンドを入力してください.')
    sys.exit()


from_file = './from/' + args[1]
to_file = './to/' + args[2]
option = len_args == 5 and args[4] == 'm'

from_exists = os.path.exists(from_file)
if not from_exists:
    print('指定されたファイルは存在しません.')
    sys.exit()

f = open(from_file, 'r')
from_json = json.load(f)

keys = list(from_json.keys())
values = list(from_json.values())

for key, value in zip(keys, values):
    tmp_key = key
    new_key = convert(tmp_key, option)
    var_decl = add_anotation(key, new_key, check_type(value))
    print(var_decl)
