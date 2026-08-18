# SQL Training (ECサイト SQL練習用リポジトリ)

SQL（INNER/LEFT/RIGHT/FULL JOIN、GROUP BY、HAVING、ウィンドウ関数等）を実践的に学習・演習するためのECサイトデータベース構築リポジトリです。

Python と SQLAlchemy を使用して SQLite3 データベース（`ecommerce.db`）をワンコマンドで初期化・データ投入できます。

---

## 🚀 クイックスタート

### 1. セットアップ & データベース作成

#### 方法 A: Windows バッチスクリプト（推奨）
```cmd
run_setup.bat
```
※ 自動で仮想環境（`venv`）作成とパッケージインストールが行われます。

#### 方法 B: 手動コマンド実行
```bash
# 依存パッケージインストール
pip install -r requirements.txt

# DB初期化 & シードデータ投入
python main.py
```

実行が完了すると、プロジェクトルートに `ecommerce.db` が自動生成されます。データを最初からやり直したい場合は再度 `python main.py` を実行するだけで初期化されます。

---

## 📁 ディレクトリ構成

```text
sql-training/
├── docs/
│   ├── table_definitions.md   # テーブル定義書（ER図・カラム定義・制約）
│   └── practice_queries.md    # 練習用SQLクエリ集（JOIN・GROUP BY・HAVING等）
├── seeds/                     # 初期登録データ (CSV)
│   ├── users.csv              # 会員データ (25件)
│   ├── categories.csv         # 商品カテゴリ (12件)
│   ├── suppliers.csv          # 仕入先メーカー (8件)
│   ├── products.csv           # 商品データ (20件)
│   ├── coupons.csv            # クーポン (6件)
│   ├── orders.csv             # 注文 (30件)
│   ├── order_items.csv        # 注文明細 (34件)
│   ├── payments.csv           # 決済データ (30件)
│   └── reviews.csv            # レビュー (23件)
├── src/
│   ├── database.py            # SQLite接続 & セッション管理
│   ├── models.py              # SQLAlchemy 2.0 ORMモデル定義
│   └── seeder.py              # CSVシードデータ投入ロジック
├── main.py                    # メイン初期化エントリポイント
├── ecommerce.db               # 生成されるSQLiteデータベース
├── requirements.txt           # 必要ライブラリ (SQLAlchemy)
└── run_setup.bat              # 自動セットアップスクリプト
```

---

## 📊 テーブル構成概要

| テーブル名 | 説明 | 特徴・学習用途 |
| :--- | :--- | :--- |
| `users` | 会員テーブル | 未購入ユーザーが存在（LEFT/RIGHT JOIN用） |
| `categories` | 商品カテゴリ | 親子階層構造（自己結合用）、商品0件のカテゴリあり |
| `suppliers` | 仕入先テーブル | 取引のない仕入先あり（FULL OUTER JOIN用） |
| `products` | 商品テーブル | 未仕入れ商品、未販売商品あり |
| `coupons` | クーポン | 未使用クーポンあり |
| `orders` | 注文テーブル | ステータス別（paid, shipped, pending, cancelled）、月別売上集計 |
| `order_items` | 注文明細 | 商品別売上集計、ランキング計算 |
| `payments` | 決済テーブル | 決済方法別集計（credit_card, paypay, cod, bank_transfer） |
| `reviews` | レビュー | 星1〜5点、平均評価（AVG）やHAVING絞り込み |

詳細なカラム定義やER図は [docs/table_definitions.md](docs/table_definitions.md) をご覧ください。

---

## 🛠️ 外部ツールでのSQL練習方法

生成された `ecommerce.db` は一般的な SQLite3 データベースファイルです。お好みのツールに接続して練習できます。

### 1. VSCode の拡張機能を使う場合
- おすすめ拡張機能: **`SQLite Viewer`** または **`SQLTools`**
- `ecommerce.db` を右クリックして開くだけでテーブルデータ閲覧やクエリ実行が可能です。

### 2. DBeaver を使う場合
1. DBeaver を起動し、「新しい接続」→「SQLite」を選択。
2. データベースファイルパスに本プロジェクトの `ecommerce.db` を指定して「完了」。
3. SQLエディタを開いてクエリを実行できます。

### 3. コマンドライン (SQLite CLI) を使う場合
```bash
sqlite3 ecommerce.db
```

---

## 💡 SQLクエリ集

すぐに試せるSQLクエリ集（INNER/LEFT/RIGHT/FULL JOIN, GROUP BY, HAVING, ウィンドウ関数）を [docs/practice_queries.md](docs/practice_queries.md) にまとめています。
