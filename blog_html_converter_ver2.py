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


def TagList(inputStr, inputIndex):
    output = ""
    name = ""
    # 次のindex
    nextIndex = inputIndex

    # nameがあれば値を取得する
    l = inputStr[inputIndex].split()

    if len(l) > 1 and l[1].find('name') >= 0:
        name = l[1]
        name = name.split("=")[1]
        a = name.find(']')
        if a >= 0:
            name = name[0:a]

    output += '<div class="list-bc">'
    if len(name) > 1:
        output += '<p>' + name + '</p>'
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

    if count == 3:
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
    s = '[code type=p]'
    m = re.search(r'type=.', s)
    output = "<pre><code>"
    if m != None:
        mode_type = m.group().split("=")[1]
        if(mode_type == 'p'):
            # pythonのコード
            output = '<div class="hcb_wrap">' + \
                '<pre class="prism undefined-numbers lang-python" data-lang="Python"><code>'
            mode = 1

    # 文言取得
    inputIndex += 1  # 次へ進める

    for i in range(1000):  # range 1000は無限ループ避け
        if inputStr[inputIndex].find('[/code]') >= 0:
            inputIndex += 1
            break
        else:
            output += inputStr[inputIndex] + '\n'
            inputIndex += 1

    if mode == 1:
        output += "</code></pre></div>"
    else:
        output += "</code></pre>"

    print(output)
    return inputIndex, output

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

        elif srcStrs[i].find('#') >= 0:
            outputString += TagH(srcStrs, i)
            i += 1

        elif srcStrs[i].find('[code') >= 0:
            nextIndex, output = TagCode(srcStrs, i)
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

        else:
            outputString += "<p>" + srcStrs[i] + "</p>"
            i += 1

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
    f = codecs.open(param[1], 'r', "utf_8_sig")
    src_txt = f.read()
    f.close()

    # htmlに変換する
    output = ConvertHtml(src_txt)

    f = codecs.open('blogOutput.txt', 'w', "utf_8_sig")  # 書き込みモードで開く
    f.write(output)  # シーケンスが引数。
    f.close()

    # デバッグ用にhtmlに書き出す
    debugOutput = '<link rel="stylesheet" type="text/css" href="sample.css"> '
    debugOutput += output
    f = codecs.open('blogHtmlOutput.html', 'w')  # 書き込みモードで開く
    f.write(debugOutput)  # シーケンスが引数。
    f.close()
