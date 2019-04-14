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

    return  nextIndex,output

def TagTkMain(inputStr, inputIndex):

    print (inputStr[inputIndex])
    #ファイル読み込む
    f = codecs.open("tk_main_setting.txt",'r')
    template = f.read()
    f.close()

    #アイコン取得
    img = GetIconSrc(inputStr[inputIndex])
    output=""

    #文言取得
    inputIndex +=1 #次へ進める

    for i in range(1000): #range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/tk_main]') >= 0:
            inputIndex +=1
            break
        else:
            output +=  inputStr[inputIndex] + '<br>'
            inputIndex +=1

    output = template % (img , output)

    return inputIndex, output


def TagTk(inputStr, inputIndex):
    
    print (inputStr[inputIndex])
    #ファイル読み込む
    f = codecs.open("tk_main_setting.txt",'r')
    template = f.read()
    f.close()

    #アイコン取得
    img = GetIconSrc(inputStr[inputIndex])
    output=""

    #モードの確認


    #文言取得
    inputIndex +=1 #次へ進める

    for i in range(1000): #range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/tk]') >= 0:
            inputIndex +=1
            break
        else:
            output +=  inputStr[inputIndex] + '<br>'
            inputIndex +=1

    output = template % (img , output)

    return inputIndex, output


def GetIconSrc(inputString):
    span = inputString.split()
    #print(span)
    #ここからIcon番号を取得する
    imgSrc = ""
    iconNo = 0
    for i in range(len(span)):
        if span[i].find("icon") >= 0:
            data = span[1]
            data = data.split("=")[1]
            
            a = data.find(']')
            
            if a >= 0:
                data = data[0:a]
            
            iconNo = data
            break
    #print(iconNo)
    if iconNo == 0:
        print ("icon番号を取得できませんでした。　%s" %inputString)
        return ""

    #iconファイルからimgのsrcを取得する
    f = open('icon_list.txt')
    line = f.readline()

    while line:
        print(line)
        data = line.split("=")

        if data[0] == iconNo:
            imgSrc = data[1]
            imgSrc = imgSrc.replace('\n','')
            imgSrc = imgSrc.replace('\r','')
            break
        line = f.readline()


    f.close()

    return imgSrc





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

    #アイコン情報を取得する
    #print(srcStrs)

    print("-----------------------------------------")

    #文字ごとの対応
    #for i in range(len(srcStrs)):
    i = 0
    while i < len(srcStrs):
        if srcStrs[i].find('[div]') >= 0 :
            outputString += "<div>"
            i +=1
        elif srcStrs[i].find('[/div]') >= 0 :
            outputString += "</div>"
            i +=1
        elif srcStrs[i].find('[list') >= 0 :
            nextIndex, output = TagList(srcStrs,i);

            print("listからの出力 %d %s" % (nextIndex, output) )
            i = nextIndex 
            outputString +=output
        elif srcStrs[i].find('[tk_main') >= 0 :
            nextIndex, output = TagTkMain(srcStrs,i);
            i = nextIndex
            outputString +=output

        elif srcStrs[i].find('[tk') >= 0 :
            nextIndex, output = TagTk(srcStrs,i);
            i = nextIndex
            outputString +=output

        else:
            outputString += "<p>" + srcStrs[i] + "</p>"
            i +=1

        #print(outputString)
        #print('\n')


    #print (beginIndex)
    #print (endIndex)

    #print(outputString)
    return outputString


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


    #htmlに変換する
    output = ConvertHtml(src_txt)

    f = codecs.open('blogOutput.txt', 'w',"utf_8_sig")  # 書き込みモードで開く
    f.write(output)  # シーケンスが引数。
    f.close()
