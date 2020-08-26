# sealed-deck-generator

## 実行環境（言語）

- python 3.6.12

## 利用しているライブラリ

- deap==1.3.1
  - https://github.com/DEAP/deap
- mtgsdk==1.3.1
  - https://github.com/MagicTheGathering/mtg-sdk-python

## 主なファイルの説明

- main.py
  - シールドデッキジェネレータ本体
- cardscores.txt
  - カード評価が書かれたファイル
- getcardlist.py
  - カードデータを https://magicthegathering.io/ から取得する

## 初回に実行する手順

- pip install -r requirements.txt
- python getcardlist.py

## 実行手順

- 入力をinput.txtとして保存する
- python main.py
- デッキがoutput.txtに出力される
