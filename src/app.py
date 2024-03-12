from flask import Flask, render_template, request, jsonify
import MeCab
import logging
import re

app = Flask(__name__)
app.json.ensure_ascii = False

app.logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)

@app.route("/", methods=["GET"])
def index():
  return render_template('index.html')

@app.route("/", methods=["POST"])
def extract_nouns():
  if not request.is_json:
    return jsonify({"status": "error", "result": "Content-Type: application/jsonで送信してください"})
  data = request.json
  if not 'text' in data:
    return jsonify({"status": "error", "result": "{'text':'解析したい文章'}のフォーマットで送信してください"})
  data = data["text"]
  tagger = MeCab.Tagger()
  nouns = []
  continuous_nouns = ""
  patern = "接頭辞|接尾辞|名詞"

  # 単語の品詞が接頭辞、接尾辞、名詞の場合、nouns配列に追加する
  # また、連続して上記品詞だった場合1単語として前の単語と連結して1要素として配列に追加する
  for word in tagger.parse(data).split("\n"):
    w = word.split("\t")
    if len(w) >= 4 and re.search(patern, w[4]):
      continuous_nouns += w[0]
    else:
      if continuous_nouns:
        nouns.append(continuous_nouns)
      continuous_nouns = ""

  return jsonify({"result": ', '.join(nouns)})
