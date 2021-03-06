# -*- coding: utf-8 -*-

"""
ブログの下書きをHTMLに変換する
"""


import sys
import codecs
import re
import html
#import misaka as m
import mistune
import argparse

"""
定数宣言
"""
UTF8_BOM = bytearray([0xEF, 0XBB, 0XBF])

#引数取得
parser = argparse.ArgumentParser(description='マークダウンもどきで書いたものをhtmlに変換する')  
parser.add_argument("-b", "--br", default=False,  help='改行は<br>にするか', type=bool)
parser.add_argument("-f", "--file_path", required=True,  help='ファイルのパス', type=str)
args = parser.parse_args()



#タグの属性を取得する
def get_element_value(find_element, input_data):
    datas = re.findall("\\w+=\\w+", input_data)
 
    rtn_value = None
    for data in datas:
        #print(data)
        if(find_element in data):
            rtn_value = data.split("=")[1]

            break
    return rtn_value

def TagList(inputStr, inputIndex):
    output = ""
    name = ""
    # 次のindex
    nextIndex = inputIndex
    type = 1

    #属性があるかチェック
    rtn = get_element_value("type", inputStr[inputIndex])
    #print(rtn)
    if(rtn != None):
        type = int(rtn)
        #print(type)

    #キャプチャの取得
    title = get_element_value("title", inputStr[inputIndex])

    if(type == 2):
        #背景があるリストを選択する
        output += '<div class="background-khaki">'
        if(title != None):
            output += '<p>' + title + '</p><hr>'
        inputIndex += 1

        output += '<ol>'
        for i in range(1000):  # range 1000は無限ループ避け
            if inputStr[inputIndex].find('[/list]') >= 0:
                inputIndex += 1
                break
            else:
                output += '<li>' + inputStr[inputIndex] + '</li>'
                inputIndex += 1

        output += '</ol>'
        output += '</div>'
    else:
        #番号をフルモノ
        output += '<div class="list-bc">'
        if(title != None):
            output += '<p>' + title + '</p><hr>'
        inputIndex += 1

        output += '<ol>'
        for i in range(1000):  # range 1000は無限ループ避け
            if inputStr[inputIndex].find('[/list]') >= 0:
                inputIndex += 1
                break
            else:
                output += '<li>' + inputStr[inputIndex] + '</li>'
                inputIndex += 1

        output += '</ol>'
        output += '</div>'

    nextIndex = inputIndex

    return nextIndex, output


def TagTkMain(inputStr, inputIndex):

    #print (inputStr[inputIndex])
    # ファイル読み込む
    f = codecs.open("tk_main_setting.txt", 'r')
    template = f.read()
    f.close()

    # アイコン取得
    img = GetIconSrc(inputStr[inputIndex])
    output = ""

    chara_name = ""
    # コメント取得
    index = inputStr[inputIndex].find("c=")
    if index >= 0:
        data = inputStr[inputIndex][index:]
        data = data.split("=")[1]
        a = data.find(']')

        if a >= 0:
            data = data[0:a]
            chara_name = data

    # 文言取得
    inputIndex += 1  # 次へ進める

    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/tk_main]') >= 0:
            inputIndex += 1
            break
        else:
            output += inputStr[inputIndex] + '<br>'
            inputIndex += 1

    output = template % (img, chara_name, output)

    return inputIndex, output



def TagTk(inputStr, inputIndex):
    # [tk mode=l   icon=1]

    # 文字列の[]を削除する
    act = inputStr[inputIndex][1:-1]

    mode = act.split()[1].split("=")[1]

    fileName = "tk_setting_l.txt"

    if(mode == 'r'):
        fileName = "tk_setting_r.txt"

    # ファイル読み込む
    f = codecs.open(fileName, 'r')
    template = f.read()
    f.close()

    # アイコン取得
    img = GetIconSrc(inputStr[inputIndex])
    output = ""

    # 文言取得
    inputIndex += 1  # 次へ進める

    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/tk]') >= 0:
            inputIndex += 1
            break
        else:
            output += inputStr[inputIndex] + '<br>'
            inputIndex += 1

    output = template % (img, output)
    # print(output)
    return inputIndex, output


def GetIconSrc(inputString):
    span = inputString.split()
    # print(span)
    # ここからIcon番号を取得する
    imgSrc = ""
    iconNo = 0
    for i in range(len(span)):
        if span[i].find("icon") >= 0:
            data = span[i]
            data = data.split("=")[1]
            a = data.find(']')

            if a >= 0:
                data = data[0:a]

            iconNo = data
            break
    # print(iconNo)

    if iconNo == 0:
        print("icon番号を取得できませんでした。　%s" % inputString)
        return ""

    # iconファイルからimgのsrcを取得する
    f = open('icon_list.txt')
    line = f.readline()
    # print(iconNo)
    while line:
        # print(line)
        data = line.split("=")

        if data[0] == iconNo:
            imgSrc = data[1]
            imgSrc = imgSrc.replace('\n', '')
            imgSrc = imgSrc.replace('\r', '')
            break
        line = f.readline()

    f.close()

    return imgSrc


def TagH(inputStr, inputIndex):
    output = ""

    # Hタグの種別判定
    count = inputStr[inputIndex].count('#')

    if count == 4:
        output = '<h5 class="hikage2">' + inputStr[inputIndex][4:] + '</h5>'
        output = '<p>' + output + '</p>'

    elif count == 3:
        output = '<h4 class="hikage2">' + inputStr[inputIndex][3:] + '</h4>'
        output = '<p>' + output + '</p>'

    elif count == 2:
        output = '<h3 class="hikage2">' + inputStr[inputIndex][2:] + '</h3>'
        output = '<p>' + output + '</p>'
    else:
        output = '<h2 class="hikage2">' + inputStr[inputIndex][1:] + '</h2>'
        output = '<p>' + output + '</p>'

    # print(output)
    return output

def TagHtml(inputStr, inputIndex):

    inputIndex += 1  # 次へ進める
    output = ""
    for i in range(100000):  # range 100000は無限ループ避け
        if inputStr[inputIndex].find('[/html]') >= 0:
            inputIndex += 1
            break
        else:
            output +=  inputStr[inputIndex]
            inputIndex += 1
    #[/html]まで進める

    return inputIndex, output

def TagQuote(inputStr, inputIndex):

    # 文言取得
    inputIndex += 1  # 次へ進める

    output = "<blockquote>"

    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/quote]') >= 0:
            inputIndex += 1
            break
        else:
            output += '<p>' + inputStr[inputIndex] + '</p>'
            inputIndex += 1

    output += "</blockquote>"

    print(output)
    return inputIndex, output


def TagCode(inputStr, inputIndex):

    # python専用のcodeかチェック
    mode = 0  # 0はデフォルト 1:pythonのコード
    s = inputStr[inputIndex]
    m = re.search(r'type=.*', s[1:-1])
    output = "<pre><code>"
    if m != None:
        mode_type = m.group().split("=")[1]
        #print(mode_type)
        if(mode_type == 'p'):
            # pythonのコード
            output = '<div class="hcb_wrap">' + \
                '<pre class="prism undefined-numbers lang-python" data-lang="Python"><code>'
            mode = 1
        elif(len(mode_type) > 0):

            output = '<div class="hcb_wrap">' + \
                '<pre class="prism undefined-numbers lang-%s" data-lang="%s"><code>' % (mode_type, mode_type)
            
            mode = 1
    else:
        #textとみなす
        pass

    # 文言取得
    inputIndex += 1  # 次へ進める

    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/code]') >= 0:
            inputIndex += 1
            break
        else:
            s = inputStr[inputIndex] 
            s = s.replace("<","&lt;")
            s = s.replace(">","&gt;")
            #s = s.replace("&","&amp;")
            output += s + '\n'
            #htmlのエスケープ
            #output = output.replace("<","&lt;")
            #output = output.replace(">","&gt;")
            inputIndex += 1

    if mode == 1:
        output += "</code></pre></div>"
    else:
        output += "</code></pre>"

    print(output)
    return inputIndex, output

# TagWaku
def TagWaku(inputStr, inputIndex):

    title_value = ""
    # タイトルがあるかチェック
    m = re.search(r'title=[^\]]*', inputStr[inputIndex])
    if m != None:
        title_value = m.group().split("=")[1]
    
    # 次に進める
    inputIndex += 1

    output = '<div class="ep-box es-BsubTradi bgc-white es-borderSolidM es-radius brc-DPred" title="%s">' %(title_value)
    nextIndex = inputIndex

    return nextIndex, output



def EndTagWaku(inputStr, inputIndex):
    # 次に進める
    inputIndex += 1

    output = '</div>'
    nextIndex = inputIndex

    return nextIndex, output

# ポイントtagsの対応
def TagPoint(inputStr, inputIndex):
    output = ""
    output += '<div class="point_box">'

    # タイトルがあるかチェック
    m = re.search(r'title=[^\]]*', inputStr[inputIndex])
    if m != None:
        title_value = m.group().split("=")[1]
        # タイトル出力
        output += '<span class="box-title">' + title_value + '</span>'

    # 次に進める
    inputIndex += 1

    # [/point]まで文字を出力
    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/point]') >= 0:
            inputIndex += 1
            break
        else:
            output += '<p>' + inputStr[inputIndex] + '</p>'
            inputIndex += 1

    output += '</div>'
    nextIndex = inputIndex

    return nextIndex, output

# Info tagsの対応


def TagInfo(inputStr, inputIndex):
    output = ""
    output += '<div class="info_box">'

    # タイトルがあるかチェック
    m = re.search(r'title=[^\]]*', inputStr[inputIndex])
    if m != None:
        title_value = m.group().split("=")[1]
        # タイトル出力
        output += '<span class="box-title">' + title_value + '</span>'

    # 次に進める
    inputIndex += 1

    # [/point]まで文字を出力
    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/info]') >= 0:
            inputIndex += 1
            break
        else:
            output += '<p>' + inputStr[inputIndex] + '</p>'
            inputIndex += 1

    output += '</div>'
    nextIndex = inputIndex

    return nextIndex, output

# 破線の対応


def TagLine(inputStr, inputIndex):
    output = ""
    output += '<div class="broken_line">'

    # 次に進める
    inputIndex += 1

    # [/point]まで文字を出力
    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/line]') >= 0:
            inputIndex += 1
            break
        else:
            output += '<p>' + inputStr[inputIndex] + '</p>'
            inputIndex += 1

    output += '</div>'
    nextIndex = inputIndex

    return nextIndex, output


def TagDiv(inputStr, inputIndex):
    # [tk mode=l   icon=1]
    output = "<div"

    # 文字列の[]を削除する
    act = inputStr[1:-1]

    # パラメータチェック
    params = act.split()
    print(params)
    if(len(params) > 1):
        temp = params[1].split("=")
        output += " %s=%s" % (temp[0], temp[1])

    output += ">"

    # print(output)
    return inputIndex, output

def TagMarkdown(inputStr, inputIndex):
    # マークダウン処理
    inputIndex += 1  # 次へ進める

    output = ""
    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/markdown]') >= 0:
            inputIndex += 1
            break
        else:
            s = inputStr[inputIndex]
            s = s + "\n"
            output +=s
            #output += mistune.html(s)
            inputIndex += 1
    output = mistune.markdown(output)
    #print(output)
    return inputIndex, output


def ConvertHtml(inputStr):

    # 出力文字列
    outputString = ""

    # 前処理
    # 行頭の.を削除する
    inputStr = re.sub('^\.', "", inputStr, flags=re.MULTILINE)

    # 改行コードで分ける
    srcStrs = inputStr.split("\n")

    # 最初の[div]の位置取得
    beginIndex = 0
    for i in range(len(srcStrs)):
        if srcStrs[i].find('[div]') >= 0:
            beginIndex = i
            break

    # 最後の[/div]の位置取得
    endIndex = 0
    for i in range(len(srcStrs)):
        if srcStrs[i].find('[/div]') >= 0:
            endIndex = i

    # 不必要な文言削除
    srcStrs = srcStrs[beginIndex:endIndex+1]

    # アイコン情報を取得する
    # print(srcStrs)

    print("-----------------------------------------")

    # 文字ごとの対応
    # for i in range(len(srcStrs)):
    i = 0
    while i < len(srcStrs):
        if srcStrs[i].find('[div') >= 0:

            nextIndex, output = TagDiv(srcStrs[i], i)
            outputString += output
            i += 1
        elif srcStrs[i].find('[/div]') >= 0:
            outputString += "</div>"
            i += 1
        elif srcStrs[i].find('[list') >= 0:
            nextIndex, output = TagList(srcStrs, i)

            print("listからの出力 %d %s" % (nextIndex, output))
            i = nextIndex
            outputString += output
        elif srcStrs[i].find('[tk_main') >= 0:
            nextIndex, output = TagTkMain(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[tk') >= 0:
            nextIndex, output = TagTk(srcStrs, i)
            i = nextIndex
            outputString += output

        #hタグ処理
        elif re.search("^\.#|^#" ,srcStrs[i]) !=None :
            outputString += TagH(srcStrs, i)
            i += 1

        #codeタグ
        elif re.search('\[code.*\]',srcStrs[i]) !=None:
            nextIndex, output = TagCode(srcStrs, i)
            i = nextIndex
            outputString += output

        #マークダウン
        elif srcStrs[i].find('[markdown]') >= 0:
            nextIndex, output = TagMarkdown(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[quote]') >= 0:
            nextIndex, output = TagQuote(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[point') >= 0:
            nextIndex, output = TagPoint(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[info') >= 0:
            nextIndex, output = TagInfo(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[html') >= 0:
            nextIndex, output = TagHtml(srcStrs, i)
            i = nextIndex
            outputString += output

        elif srcStrs[i].find('[line]') >= 0:
            nextIndex, output = TagLine(srcStrs, i)
            i = nextIndex
            outputString += output

        #wakuタグ追加
        elif srcStrs[i].find('[waku') >= 0:
            nextIndex, output = TagWaku(srcStrs, i)
            i = nextIndex
            outputString += output

        #waku終了タグ追加
        elif srcStrs[i].find('[/waku') >= 0:
            nextIndex, output = EndTagWaku(srcStrs, i)
            i = nextIndex
            outputString += output

        else:
            outputString += "<p>" + srcStrs[i] + "</p>"
            i += 1

        outputString = outputString + "\n"
        # print(outputString)
        # print('\n')

        # ここにpoint用、info用を追加する
        # あと親子リスト

    #print (beginIndex)
    #print (endIndex)

    # print(outputString)
    return outputString


if __name__ == '__main__':
    # 変換の元ファイルを読み込む
    param = sys.argv
    if (len(param) == 0):
        print("Usage: $ python " + param[0] + " number")
        quit()

    # UTF-8のBOMの考慮
    f = codecs.open(args.file_path, 'r', "utf_8_sig")
    src_txt = f.read()
    f.close()

    # htmlに変換する
    output = ConvertHtml(src_txt)

    # 改行をbrに変換するか
    if(args.br == True):
        print("改行を<br>に変換します")
        output = output.replace('<p></p>', '<br>')

    f = codecs.open('blogOutput.txt', 'w', "utf_8_sig")  # 書き込みモードで開く
    f.write(output)  # シーケンスが引数。
    f.close()

    # デバッグ用にhtmlに書き出す
    debugOutput = '<link rel="stylesheet" type="text/css" href="sample.css"> '
    debugOutput += output
    f = codecs.open('blogHtmlOutput.html', 'w')  # 書き込みモードで開く
    f.write(debugOutput)  # シーケンスが引数。
    f.close()
