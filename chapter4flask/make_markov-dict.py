import requests  # ❶requestsをインポート
from tqdm import tqdm
import io  # ❶モジュールをインポート
import zipfile
import re
import pickle
import requests  # ❶requestsをインポート
from collections import Counter, defaultdict
from janome.tokenizer import Tokenizer

BEGIN = '__BEGIN__'  # 文の開始マーク
END = '__END__'  # 文の終了マーク

def get_three_words_list(sentence):  # ❶ 関数にする
    """文章を3単語の組にして返す"""
    t = Tokenizer()
    words = list(t.tokenize(sentence, wakati=True))
    words = [BEGIN] + words + [END]
    three_words_list = []
    for i in range(len(words) - 2):
        three_words_list.append(tuple(words[i:i+3]))
    return three_words_list


def generate_markov_dict(three_words_count):
    """マルコフ連鎖での文章生成用の辞書データを生成する"""
    markov_dict = {}
    for three_words, count in three_words_count.items():
        two_words = three_words[:2]  # ❶ 「前半2つの単語」と「次の単語」に分割
        next_word = three_words[2]
        if two_words not in markov_dict: # ❷ 辞書に存在しない場合は空データを生成
            markov_dict[two_words] = {'words': [], 'weights': []}
        markov_dict[two_words]['words'].append(next_word)  # ❸ 次の単語と回数を追加
        markov_dict[two_words]['weights'].append(count)
    return markov_dict


def get_first_words_weights(three_words_count):
    """最初の単語を選択するための辞書データを作成する"""
    first_word_count = defaultdict(int)

    for three_words, count in three_words_count.items():
        if three_words[0] == BEGIN:
            next_word = three_words[1]
            first_word_count[next_word] += count

    words = []  # ❶ 単語と重み(出現回数)を格納するリスト
    weights = []
    for word, count in first_word_count.items():
        words.append(word)  # ❷ 単語と重みをリストに追加
        weights.append(count)

    return words, weights

# 「人間失格」のファイルのURL
url = 'https://www.aozora.gr.jp/cards/000035/files/301_ruby_5915.zip'
r = requests.get(url)  # ❷ZipファイルのURLアクセス
content = r.content  # ❸Zipファイルの中身を取得

f = io.BytesIO(content)  # ❷バイナリをファイルのように変換
zipf = zipfile.ZipFile(f)  # ❸Zipファイルを開く
namelist = zipf.namelist()  # ❹ファイル一覧を取得
print(namelist)

data = zipf.read(namelist[0])  # ❶Zipファイルを展開しデータを取り出す
original_text = data.decode('Shift_JIS')  # ❷文字列にデコードする
print(original_text[:500])  # ❸中身を確認する

first_sentence = '私は、その男の写真を三葉、見たことがある。'
last_sentence = '神様みたいないい子でした'
_, text = original_text.split(first_sentence)  # ❶ 青空文庫の説明文を削除
text, _ = text.split(last_sentence)
text = first_sentence + text + last_sentence

text = text.replace('｜', '').replace('　', '')  # ❷ '｜'' と '　' を削除
text = re.sub('《\w+》', '', text)  # ❷ルビを削除
text = re.sub('［＃\w+］', '', text)  # ❷注を削除
text = text.replace('\r', '').replace('\n', '')  # ❷改行文字を削除
text = re.sub('[、「」？]', '', text)  # ❷、「」 ？を削除
text = re.sub('（\w+）', '', text)  # ❷（）と［］で囲まれている文を削除
text = re.sub('［\w+］', '', text)

sentences = text.split('。')  # ❸。で文章を分割
print('文の数:', len(sentences))
print(sentences[:10])

three_words_list = []
for sentence in tqdm(sentences):  # ❶ tqdmで進捗バーを表示する
    three_words_list += get_three_words_list(sentence)
three_words_count = Counter(three_words_list)
len(three_words_count)  # ❷ 3単語の組の種類を確認

markov_dict = generate_markov_dict(three_words_count)  # ❶ 文章生成用の辞書データを作成
print(len(markov_dict))
first_words, first_weights = get_first_words_weights(three_words_count)  # ❷最初の単語と出現数を取得
print(len(first_words))

print(first_words)
with open('markov-dict.pickle', 'wb') as f:  # ❶ファイルをバイナリ書き込みモードで開く
    data = (first_words, first_weights, markov_dict)  # ❷3つのデータをタプルにまとめる
    pickle.dump(data, f)  # ➌dataをpickle化して書き込む
