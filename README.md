# 名詞抽出API
WIP: 実装途中とREADMEも内容拡充前swaggerとかでまとめたい

## 概要

POSTで送った文章から名詞を抽出して配列で返すAPI  
連続した名詞は1つの単語として配列中の1要素として返す。

## 起動手順

```bash
docker build -t extract-nouns:latest .
docker run -d -p 5000:5000 -v /path/to/extract-nouns/src:/usr/src extract-nouns:latest
```

`curl -X POST -H "Content-Type: application/json" -d '{"text": "お試しの文章を入力してみます"}' http://localhost:5000/`を実行すると`{"result": ["お試し", "文章", "入力"]}`が返ってくる
