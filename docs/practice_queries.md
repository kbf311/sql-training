# SQL実践練習クエリ（出題編）

本ドキュメントでは、ECサイトデータベース（`ecommerce.db`）に対して外部ツール（DBeaver, VSCode SQLite Viewer, SQLite CLI等）で実行できる実践的なSQL演習問題を掲載しています。

解答・解説は [docs/solutions/practice_queries_answers.md](solutions/practice_queries_answers.md) にまとめています。まずは自力でクエリを作成してみて、詰まった際や答え合わせに参照してください。

---

## 目次
1. [テーブル結合 (JOIN)](#1-テーブル結合-join)
   - [1.1 INNER JOIN (内部結合)](#11-inner-join-内部結合)
   - [1.2 LEFT JOIN (左外部結合) - 未購入ユーザー](#12-left-join-左外部結合---未購入ユーザー)
   - [1.3 LEFT JOIN (左外部結合) - 未レビュー商品](#13-left-join-左外部結合---未レビュー商品)
   - [1.4 RIGHT JOIN (右外部結合) - 商品未登録の仕入先](#14-right-join-右外部結合---商品未登録の仕入先)
   - [1.5 FULL OUTER JOIN (完全外部結合) - 仕入先・商品の未紐付け](#15-full-outer-join-完全外部結合---仕入先商品の未紐付け)
   - [1.6 自己結合 (Self JOIN) - カテゴリ階層](#16-自己結合-self-join---カテゴリ階層)
2. [集計と絞り込み (GROUP BY / HAVING)](#2-集計と絞り込み-group-by--having)
   - [2.1 都道府県別の会員数と購入総額](#21-都道府県別の会員数と購入総額)
   - [2.2 複数回購入しているリピーター会員の抽出 (HAVING)](#22-複数回購入しているリピーター会員の抽出-having)
   - [2.3 平均評価が4.0以上の高評価商品の抽出 (HAVING)](#23-平均評価が40以上の高評価商品の抽出-having)
   - [2.4 月別売上高と注文件数の集計](#24-月別売上高と注文件数の集計)
3. [サブクエリ・ウィンドウ関数 (応用)](#3-サブクエリウィンドウ関数-応用)
   - [3.1 全体平均より高い商品のみ抽出 (サブクエリ)](#31-全体平均より高い商品のみ抽出-サブクエリ)
   - [3.2 カテゴリごとの売上ランキング (ウィンドウ関数 RANK)](#32-カテゴリごとの売上ランキング-ウィンドウ関数-rank)
   - [3.3 累計売上の算出 (ウィンドウ関数 SUM OVER)](#33-累計売上の算出-ウィンドウ関数-sum-over)

---

## 1. テーブル結合 (JOIN)

### 1.1 INNER JOIN (内部結合)
> **お題**: 注文が存在する会員の名前、注文日、合計金額、決済ステータスを取得する。  
> 注文日（`order_date`）の降順で並び替えてください。

- **対象テーブル**: `users`, `orders`, `payments`
- **ヒント**: `users` と `orders`、および `orders` と `payments` を `INNER JOIN` で結合します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#11-inner-join-内部結合)

---

### 1.2 LEFT JOIN (左外部結合) - 未購入ユーザー
> **お題**: 一度も注文をしたことがない会員（未購入ユーザー）のID、名前、メールアドレス、登録日時を検出する。

- **対象テーブル**: `users`, `orders`
- **ヒント**: `users` を主テーブルにして `orders` を `LEFT JOIN` し、注文ID（`orders.id`）が `NULL` となる行を `WHERE` で絞り込みます。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#12-left-join-左外部結合---未購入ユーザー)

---

### 1.3 LEFT JOIN (左外部結合) - 未レビュー商品
> **お題**: レビューがまだ1件も投稿されていない商品（ID、商品名、価格）一覧を取得する。

- **対象テーブル**: `products`, `reviews`
- **ヒント**: `products` に `reviews` を `LEFT JOIN` し、レビューID（`reviews.id`）が `NULL` である条件を指定します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#13-left-join-左外部結合---未レビュー商品)

---

### 1.4 RIGHT JOIN (右外部結合) - 商品未登録の仕入先
> **お題**: 取り扱い商品がまだ登録されていない仕入先（メーカー）のID、仕入先名、国を検出する。

- **対象テーブル**: `products`, `suppliers`
- **ヒント**: `products` と `suppliers` を `RIGHT JOIN` で結合し、商品名または商品IDが `NULL` のレコードを抽出します。（※ SQLite 3.39.0 以降で対応）
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#14-right-join-右外部結合---商品未登録の仕入先)

---

### 1.5 FULL OUTER JOIN (完全外部結合) - 仕入先・商品の未紐付け
> **お題**: 「仕入先未設定の商品」および「商品が登録されていない仕入先」を両方網羅して取得する。

- **対象テーブル**: `products`, `suppliers`
- **ヒント**: `FULL OUTER JOIN` を行い、商品IDが `NULL` または仕入先IDが `NULL` の行を抽出します。（※ SQLite 3.39.0 以降で対応）
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#15-full-outer-join-完全外部結合---仕入先商品の未紐付け)

---

### 1.6 自己結合 (Self JOIN) - カテゴリ階層
> **お題**: カテゴリテーブルを自己結合して、子カテゴリID、子カテゴリ名、親カテゴリ名を並べて表示する。  
> 親カテゴリが存在しない最上位カテゴリの場合は `'（最上位カテゴリ）'` と表示させてください。

- **対象テーブル**: `categories`
- **ヒント**: `categories` テーブルに別名（エイリアス）`child` と `parent` を付けて `LEFT JOIN` します。`COALESCE` 関数を使うと `NULL` の代替表示ができます。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#16-自己結合-self-join---カテゴリ階層)

---

## 2. 集計と絞り込み (GROUP BY / HAVING)

### 2.1 都道府県別の会員数と購入総額
> **お題**: 都道府県ごとの会員数（重複なし）、その都道府県の会員による総購入金額、注文件数を集計する。  
> 購入総額の降順で並び替えてください（購入が0件の都道府県も0として表示）。

- **対象テーブル**: `users`, `orders`
- **ヒント**: `u.prefecture` で `GROUP BY` を行います。会員数は `COUNT(DISTINCT u.id)` を使用します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#21-都道府県別の会員数と購入総額)

---

### 2.2 複数回購入しているリピーター会員の抽出 (HAVING)
> **お題**: 注文回数が2回以上で、合計購入額が20,000円以上の優良リピーター会員（ID、名前、メール、注文数、合計金額、平均注文金額）を抽出する。  
> 対象注文ステータスは `'paid'`, `'shipped'` とします。

- **対象テーブル**: `users`, `orders`
- **ヒント**: 注文ステータスの絞り込みは `WHERE` 句で行い、集計後の条件（注文数 >= 2、合計金額 >= 20000）は `HAVING` 句で指定します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#22-複数回購入しているリピーター会員の抽出-having)

---

### 2.3 平均評価が4.0以上の高評価商品の抽出 (HAVING)
> **お題**: レビューが2件以上投稿されており、かつ平均評価（星）が4.0以上の商品（ID、商品名、価格、レビュー件数、平均評価）を取得する。  
> 平均評価の降順、レビュー件数の降順で並び替えてください。

- **対象テーブル**: `products`, `reviews`
- **ヒント**: 商品ごとに `GROUP BY` し、`HAVING` 句で `COUNT(r.id) >= 2` かつ `AVG(r.rating) >= 4.0` を判定します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#23-平均評価が40以上の高評価商品の抽出-having)

---

### 2.4 月別売上高と注文件数の集計
> **お題**: 注文年月（YYYY-MM）ごとに、注文件数・売上合計・平均客単価を集計する。  
> キャンセルされた注文（`status = 'cancelled'`）は除外してください。

- **対象テーブル**: `orders`
- **ヒント**: SQLite では `strftime('%Y-%m', order_date)` で年月を取り出して `GROUP BY` に指定します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#24-月別売上高と注文件数の集計)

---

## 3. サブクエリ・ウィンドウ関数 (応用)

### 3.1 全体平均より高い商品のみ抽出 (サブクエリ)
> **お題**: 全商品の平均販売価格よりも高い商品一覧（商品名、価格、全体平均価格、平均との差額）を取得する。

- **対象テーブル**: `products`
- **ヒント**: `(SELECT AVG(price) FROM products)` をスカラサブクエリとして `SELECT` 句と `WHERE` 句で活用します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#31-全体平均より高い商品のみ抽出-サブクエリ)

---

### 3.2 カテゴリごとの売上ランキング (ウィンドウ関数 RANK)
> **お題**: カテゴリごとに、商品の売上金額ランキングを算出する（カテゴリ名、商品名、総販売数量、総売上金額、カテゴリ内順位）。

- **対象テーブル**: `categories`, `products`, `order_items`
- **ヒント**: CTE（`WITH` 句）で商品ごとの売上を集計した後、`DENSE_RANK() OVER (PARTITION BY category_name ORDER BY total_revenue DESC)` を適用します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#32-カテゴリごとの売上ランキング-ウィンドウ関数-rank)

---

### 3.3 累計売上の算出 (ウィンドウ関数 SUM OVER)
> **お題**: 日別の売上合計と、最初の日からの累積売上推移を計算する。  
> 対象注文ステータスは `'paid'`, `'shipped'` とします。

- **対象テーブル**: `orders`
- **ヒント**: 日別売上を CTE でまとめた上で、`SUM(daily_amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` を使って累積和を計算します。
- [👉 回答・解説を確認する](solutions/practice_queries_answers.md#33-累計売上の算出-ウィンドウ関数-sum-over)
