# BlogHtmlConverte Ver2

#概要
マークダウンのように書いたテキスト文章を
Html形式に変換してくれるツール。
通常の文字列は原則<p></p>に変換されます。

# 実行方法


# タグの意味
* [div]・・・div要素。文章の最初と終わりには必ず必要
* [list name="タイトル"]
リスト表示する。nameは省略できる。
格納先ファイル名・・・setting_list.txt


*[code]
ソースコードを書く。
*[quote]
引用文

*[tk mode=l   icon=1]
会話文形式のhtmlを作成する。
mode:
l・・・left　左側
r・・・right　右側

icon:
使うイメージ番号
imgのurlは別資料

格納先ファイル：
左側・・・tk_setting_l.txt
右側・・・tk_setting_r.txt


*[tk_main  icon=1]
一つだけの会話のような吹き出し
アイコンの大きさが「tk」よりも大きい
格納先ファイル：
tk_main_setting.txt

*[text_ad]
テキストの広告
格納先ファイル名・・・text_ad.txt


*[img_ad]
画像広告
格納先ファイル名・・・img_ad.txt

アイコンの設定ファイル
icon_list.txt

# 注意事項
(1)変換後の文字はハードコーディングです。
このソースコードを実際に使うには、ハードコーディングの部分を修正する必要がある。

(2)タグの入れ子には対応していません。
