# -*- coding: utf-8 -*-

"""
ブログの下書きをHTMLに変換する
"""


import sys
import codecs
import re


"""
定数宣言
"""
UTF8_BOM = bytearray([0xEF, 0XBB, 0XBF])

KIND_NO_AREA = 0
KIND_DIV_AREA = 1
KIND_TALK_Q_AREA = 2
KIND_TALK_A_AREA = 3
KIND_LIST_1 = 4
KIND_DIV_WAKU = 5
KIND_AD_AREA = 6
KIND_CODE = 7
KIND_QUOTE = 8

MODE_LIST_1 = 1
MODE_CODE = 2
MODE_QUOTE = 3

"""
StrBlock型の変数にデータをセットする
ブロック要素
[div]
[talk_q]
[talk_a]
[list_1]
[div_waku]
[ad]
[code]
[blockquote]
"""


def TagList(inputStr, inputIndex):
    output=""
    name = ""
    #次のindex
    nextIndex = inputIndex

    #nameがあれば値を取得する
    l = inputStr[inputIndex].split()
    print(l)
    if len(l) > 1 and  l[1].find('name') >= 0 :
        name = l[1]
        name = name.split("=")[1]
        a = name.find(']')
        if a >= 0:
            name = name[0:a]

    output += '<div class="list-bc">'
    if len(name) > 1:
        output +=  '<p>' + name + '</p>'
        inputIndex +=1


    output += '<ol>'
    for i in range(1000): #range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/list]') >= 0:
            inputIndex +=1
            break
        else:
            output +=  '<li>' + inputStr[inputIndex] + '</li>'
            inputIndex +=1

    output += '</ol>'
    output += '</div>'
    nextIndex = inputIndex

    print(output)
    return  nextIndex,output
           
def ConvertHtml(inputStr):

    #出力文字列
    outputString = ""
    
    #前処理
    #行頭の.を削除する
    inputStr = re.sub('^\.', "", inputStr,flags=re.MULTILINE)

    #改行コードで分ける
    srcStrs =  inputStr.split("\n")
    
    #最初の[div]の位置取得
    beginIndex = 0
    for i in range(len(srcStrs)):
        if srcStrs[i].find('[div]') >= 0 :
            beginIndex = i
            break;
    

    #最後の[/div]の位置取得
    endIndex = 0
    for i in range(len(srcStrs)):
        if srcStrs[i].find('[/div]') >= 0 :
            endIndex = i

    #不必要な文言削除
    srcStrs = srcStrs[beginIndex:endIndex+1]

    #print(srcStrs)

    print("-----------------------------------------")

    #文字ごとの対応
    for i in range(len(srcStrs)):
        if srcStrs[i].find('[div]') >= 0 :
            outputString += "<div>"
        
        elif srcStrs[i].find('[/div]') >= 0 :
            outputString += "</div>"
        
        elif srcStrs[i].find('[list') >= 0 :
           nextIndex, output = TagList(srcStrs,i);
           i = nextIndex
           outputString +=output
        else:
            outputString += "<p>" + srcStrs[i] + "</p>"

        #print(outputString)
        #print('\n')


    print (beginIndex)
    print (endIndex)

    print(outputString)
    return "aaa"


if __name__ == '__main__':
    # 変換の元ファイルを読み込む
    param = sys.argv
    if (len(param) == 0):
        print ("Usage: $ python " + param[0] + " number")
        quit()

    #UTF-8のBOMの考慮
    f = codecs.open(param[1],'r',"utf_8_sig")
    src_txt = f.read()
    f.close()

#print(src_txt)

    #htmlに変換する
    output = ConvertHtml(src_txt)



"""
    #入力文字を分類する
    for i in range(len(blocks)):
        block = blocks[i]
        print("-----------------------------------------")
        print block



    print output
    f = codecs.open('blogOutput.txt', 'w',"utf_8_sig")  # 書き込みモードで開く
    f.write(output)  # シーケンスが引数。
    f.close()

"""
