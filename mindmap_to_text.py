#!/usr/bin/env python
# coding: utf-8
import argparse

#マインドマップ形式の文字列をブログ下書き用のフォーマットに変換する
#xmindでマインドマップ作成⇒コピーしてテキストへ⇒本ツールで変換

#ルール
#タブ一つが「#」に該当する
#現在のタブ位置と次のタブ位置が同じ場合は、#を出さない

#引数取得
parser = argparse.ArgumentParser(description='マインドマップ形式の文字列をブログ下書き用のフォーマットに変換する')  
parser.add_argument("-f", "--file_path", required=True,  help='ファイルのパス', type=str)
args = parser.parse_args()

#ファイルを読み込む
f = open(args.file_path, 'r')
data = f.read()

src_text_list  = data.split('\n')




pre_line = {}
next_line = {}

#一行目は狙っているキーワードを格納
text_list_out = []
text_list_out.append(src_text_list[0])

filename = src_text_list[0]

#２行目から処理開始
src_text_list = src_text_list[1:]
limit_cnt = len(src_text_list)



for index, text in enumerate(src_text_list):
    
    #最終行？
    #print(index, limit_cnt)
    if(index == limit_cnt -1):
        #最終行はそのままのテキストを出力
        data = text.replace("\t", "")
        text_list_out.append(data)
        break
    
    #次の行のデータも取得
    next_line = {"text":src_text_list[index+1], "tab_cnt": src_text_list[index+1].count("\t")}


    #tab_cntの数による処理分岐
    
    #現在と次が同じtab数
    now_tab_cnt = src_text_list[index].count("\t")
    
    if(now_tab_cnt < next_line["tab_cnt"] ):
        data = text.replace("\t", "#")
    else:
        data = text.replace("\t", "")
        
    text_list_out.append(data)



#レンダリング
filename = filename + 'mindmap.txt'
f = open(filename, 'w', encoding='utf_8_sig')

write_text = []

write_text.append("■狙っているキーワード\n")

for text in text_list_out:
    
    # #がある時の対処
    tmp = ""
    if("#" in text):
        tmp = "\n."
    text = tmp + text + "\n"
    write_text.append(text)

f.writelines(write_text)
f.close()


# In[ ]:




