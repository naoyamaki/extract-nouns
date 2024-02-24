from flask import Flask, render_template, request, jsonify
import MeCab
import logging, sys
import re

app = Flask(__name__)
app.json.ensure_ascii = False

app.logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

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


# curl -X POST -H "Content-Type: application/json" -d "{'text': 'お試しの文章を入力してみます'}" http://localhost:5000/
# 上記のようなリクエストを送った時は
# tagger.parse(data).split("\n")は['お\tオ\tオ\t御\t接頭辞\t\t\t', '試し\tタメシ\tタメシ\t試し\t名詞-普通名詞-一般\t\t\t3', 'の\tノ\tノ\tの\t助詞-格助詞\t\t\t', '文章\tブンショー\tブンショウ\t文章\t名詞-普通名詞-一般\t\t\t1', 'を\tオ\tヲ\tを\t助詞-格助詞\t\t\t', '入力\tニューリョク\tニュウリョク\t入力\t名詞-普通名詞-サ変可能\t\t\t0,1', 'し\tシ\tスル\t為る\t動詞-非自立可能\tサ行変格\t連用形-一般\t0', 'て\tテ\tテ\tて\t助詞-接続助詞\t\t\t', 'み\tミ\tミル\t見る\t動詞-非自立可能\t上一段-マ行\t連用形-一般\t1', 'ます\tマス\tマス\tます\t助動詞\t助動詞-マス\t終止形-一般\t', 'EOS', '']
# となり、wordは
# ['お', 'オ', 'オ', '御', '接頭辞', '', '', ''], 
# ['試し', 'タメシ', 'タメシ', '試し', '名詞-普通名詞-一般', '', '', '3'], 
# ['の', 'ノ', 'ノ', 'の', '助詞-格助詞', '', '', ''], 
# ['文章', 'ブンショー', 'ブンショウ', '文章', '名詞-普通名詞-一般', '', '', '1'], 
# ['を', 'オ', 'ヲ', 'を', '助詞-格助詞', '', '', ''], 
# ['入力', 'ニューリョク', 'ニュウリョク', '入力', '名詞-普通名詞-サ変可能', '', '', '0,1'], 
# ['し', 'シ', 'スル', '為る', '動詞-非自立可能', 'サ行変格', '連用形-一般', '0'], 
# ['て', 'テ', 'テ', 'て', '助詞-接続助詞', '', '', ''], 
# ['み', 'ミ', 'ミル', '見る', '動詞-非自立可能', '上一段-マ行', '連用形-一般', '1'], 
# ['ます', 'マス', 'マス', 'ます', '助動詞', '助動詞-マス', '終止形-一般', ''], 
# ['EOS'], 
# ['']
# のようになる
