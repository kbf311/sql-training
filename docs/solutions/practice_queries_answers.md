# SQL実践練習クエリ 回答・解説編

本ドキュメントでは、[docs/practice_queries.md](../practice_queries.md) に掲載されている演習問題の**模範解答SQLクエリ**および**解説**を掲載しています。

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
> **問題**: 注文が存在する会員の名前、注文日、合計金額、決済ステータスを取得する。  
> [🔙 問題に戻る](../practice_queries.md#11-inner-join-内部結合)

#### 模範解答
```sql
SELECT 
    u.id AS user_id,
    u.name AS user_name,
    o.id AS order_id,
    o.order_date,
    o.total_amount,
    p.payment_method,
    p.payment_status
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN payments p ON o.id = p.order_id
ORDER BY o.order_date DESC;
```

#### 解説
- `users` と `orders` を `user_id` で結合し、さらに `payments` を `order_id` で多段結合しています。
- `INNER JOIN` を使用しているため、注文のないユーザーや決済情報のない注文は除外され、3つのテーブルすべてにデータが揃っているレコードのみが取得されます。

---

### 1.2 LEFT JOIN (左外部結合) - 未購入ユーザー
> **問題**: 一度も注文をしたことがない会員（未購入ユーザー）を検出する。  
> [🔙 問題に戻る](../practice_queries.md#12-left-join-左外部結合---未購入ユーザー)

#### 模範解答
```sql
SELECT 
    u.id,
    u.name,
    u.email,
    u.registered_at,
    o.id AS order_id
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

#### 解説
- `LEFT JOIN` で `users` に `orders` を結合すると、注文履歴がないユーザーの場合 `orders` 側のカラムはすべて `NULL` になります。
- `WHERE o.id IS NULL` で絞り込むことで、「一度も注文したことがないユーザー（差集合）」を抽出できます。

---

### 1.3 LEFT JOIN (左外部結合) - 未レビュー商品
> **問題**: レビューがまだ1件も投稿されていない商品一覧を取得する。  
> [🔙 問題に戻る](../practice_queries.md#13-left-join-左外部結合---未レビュー商品)

#### 模範解答
```sql
SELECT 
    p.id,
    p.name,
    p.price,
    r.id AS review_id
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id
WHERE r.id IS NULL;
```

#### 解説
- 商品テーブル `products` に対してレビューテーブル `reviews` を外部結合し、`reviews.id IS NULL` でレビュー未投稿の商品を抽出します。

---

### 1.4 RIGHT JOIN (右外部結合) - 商品未登録の仕入先
> **問題**: 取り扱い商品がまだ登録されていない仕入先（メーカー）を検出する。  
> [🔙 問題に戻る](../practice_queries.md#14-right-join-右外部結合---商品未登録の仕入先)

#### 模範解答
```sql
SELECT 
    p.name AS product_name,
    s.id AS supplier_id,
    s.name AS supplier_name,
    s.country
FROM products p
RIGHT JOIN suppliers s ON p.supplier_id = s.id
WHERE p.id IS NULL;
```

#### 解説
- 右側のテーブル `suppliers` を基準として残し、左側の `products` を結合します。
- `WHERE p.id IS NULL` を指定することで、商品がまだ紐付いていない仕入先を特定できます。
- ※ SQLite 3.39.0 以降で RIGHT JOIN / FULL OUTER JOIN がサポートされています。

---

### 1.5 FULL OUTER JOIN (完全外部結合) - 仕入先・商品の未紐付け
> **問題**: 「仕入先未設定の商品」および「商品が登録されていない仕入先」を両方網羅して取得する。  
> [🔙 問題に戻る](../practice_queries.md#15-full-outer-join-完全外部結合---仕入先商品の未紐付け)

#### 模範解答
```sql
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    s.id AS supplier_id,
    s.name AS supplier_name
FROM products p
FULL OUTER JOIN suppliers s ON p.supplier_id = s.id
WHERE p.id IS NULL OR s.id IS NULL;
```

#### 解説
- `FULL OUTER JOIN` は左右両方のテーブルのすべてのレコードを保持します。
- `WHERE p.id IS NULL OR s.id IS NULL` を加えることで、両者でマッチしなかった不一致レコード（不完全な関連付け）のみを抽出できます。

---

### 1.6 自己結合 (Self JOIN) - カテゴリ階層
> **問題**: カテゴリテーブルを自己結合して、子カテゴリ名と親カテゴリ名を並べて表示する。  
> [🔙 問題に戻る](../practice_queries.md#16-自己結合-self-join---カテゴリ階層)

#### 模範解答
```sql
SELECT 
    child.id AS sub_category_id,
    child.name AS sub_category_name,
    COALESCE(parent.name, '（最上位カテゴリ）') AS parent_category_name
FROM categories child
LEFT JOIN categories parent ON child.parent_id = parent.id
ORDER BY parent.id, child.id;
```

#### 解説
- 同一の `categories` テーブルを `child`（子）と `parent`（親）という異なるエイリアスで参照し、`child.parent_id = parent.id` で結合します。
- 最上位（ルート）カテゴリは `parent_id` が `NULL` となるため、`LEFT JOIN` を使い、`COALESCE` で `NULL` 時の表示文字を設定しています。

---

## 2. 集計と絞り込み (GROUP BY / HAVING)

### 2.1 都道府県別の会員数と購入総額
> **問題**: 都道府県ごとの会員数と、その都道府県の会員による総購入金額・注文件数を集計する。  
> [🔙 問題に戻る](../practice_queries.md#21-都道府県別の会員数と購入総額)

#### 模範解答
```sql
SELECT 
    u.prefecture,
    COUNT(DISTINCT u.id) AS user_count,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_sales
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.prefecture
ORDER BY total_sales DESC;
```

#### 解説
- ユーザーごとに複数件の注文があるため、会員数は `COUNT(DISTINCT u.id)` で重複排除してカウントします。
- 注文がまだない都道府県の会員も集計対象に含めるため `LEFT JOIN` を使用し、合計金額が `NULL` にならないよう `COALESCE` で0埋めしています。

---

### 2.2 複数回購入しているリピーター会員の抽出 (HAVING)
> **問題**: 注文回数が2回以上で、合計購入額が20,000円以上の優良リピーターを抽出する。  
> [🔙 問題に戻る](../practice_queries.md#22-複数回購入しているリピーター会員の抽出-having)

#### 模範解答
```sql
SELECT 
    u.id AS user_id,
    u.name AS user_name,
    u.email,
    COUNT(o.id) AS order_count,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status IN ('paid', 'shipped')
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) >= 2 AND SUM(o.total_amount) >= 20000
ORDER BY total_spent DESC;
```

#### 解説
- `WHERE` 句では集計前のレコード（キャンセル注文の除外など）を絞り込みます。
- `GROUP BY` でユーザー単位に集約後、集計関数（`COUNT` や `SUM`）に対する条件判定は `HAVING` 句で行います。

---

### 2.3 平均評価が4.0以上の高評価商品の抽出 (HAVING)
> **問題**: レビューが2件以上投稿されており、かつ平均評価（星）が4.0以上の商品を取得する。  
> [🔙 問題に戻る](../practice_queries.md#23-平均評価が40以上の高評価商品の抽出-having)

#### 模範解答
```sql
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.price,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM products p
INNER JOIN reviews r ON p.id = r.product_id
GROUP BY p.id, p.name, p.price
HAVING COUNT(r.id) >= 2 AND AVG(r.rating) >= 4.0
ORDER BY avg_rating DESC, review_count DESC;
```

#### 解説
- `reviews` を商品IDでグルーピングし、件数 `COUNT(r.id)` と平均 `AVG(r.rating)` を算出します。
- 「レビュー件数2件以上」かつ「平均4.0以上」という集計値に対するフィルターを `HAVING` 句で指定します。

---

### 2.4 月別売上高と注文件数の集計
> **問題**: 注文年月（YYYY-MM）ごとに、注文件数・売上合計・平均客単価を集計する。  
> [🔙 問題に戻る](../practice_queries.md#24-月別売上高と注文件数の集計)

#### 模範解答
```sql
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(id) AS total_orders,
    SUM(total_amount) AS monthly_sales,
    ROUND(AVG(total_amount), 0) AS avg_order_value
FROM orders
WHERE status NOT IN ('cancelled')
GROUP BY strftime('%Y-%m', order_date)
ORDER BY order_month ASC;
```

#### 解説
- SQLite では `strftime('%Y-%m', order_date)` を利用して日付文字列から年月部分を抽出できます。
- その年月値で `GROUP BY` を行い、売上合計や平均値を集計しています。

---

## 3. サブクエリ・ウィンドウ関数 (応用)

### 3.1 全体平均より高い商品のみ抽出 (サブクエリ)
> **問題**: 全商品の平均販売価格よりも高い商品一覧と、平均との価格差を取得する。  
> [🔙 問題に戻る](../practice_queries.md#31-全体平均より高い商品のみ抽出-サブクエリ)

#### 模範解答
```sql
SELECT 
    name,
    price,
    ROUND((SELECT AVG(price) FROM products), 0) AS overall_avg_price,
    price - ROUND((SELECT AVG(price) FROM products), 0) AS diff_from_avg
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;
```

#### 解説
- スカラサブクエリ `(SELECT AVG(price) FROM products)` を使用して全体の平均価格を算出し、`SELECT` 句での価格差の計算や `WHERE` 句での条件判定に活用しています。

---

### 3.2 カテゴリごとの売上ランキング (ウィンドウ関数 RANK)
> **問題**: カテゴリごとに、商品の売上数量ランキングを算出する。  
> [🔙 問題に戻る](../practice_queries.md#32-カテゴリごとの売上ランキング-ウィンドウ関数-rank)

#### 模範解答
```sql
WITH product_sales AS (
    SELECT 
        c.name AS category_name,
        p.name AS product_name,
        COALESCE(SUM(oi.quantity), 0) AS total_units_sold,
        COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    LEFT JOIN order_items oi ON p.id = oi.product_id
    GROUP BY c.id, c.name, p.id, p.name
)
SELECT 
    category_name,
    product_name,
    total_units_sold,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY category_name ORDER BY total_revenue DESC) AS rank_in_category
FROM product_sales
ORDER BY category_name, rank_in_category;
```

#### 解説
- 共通テーブル式（CTE: `WITH` 句）で商品ごとの売上合計と売上数量を集計します。
- `DENSE_RANK() OVER (PARTITION BY category_name ORDER BY total_revenue DESC)` を使うことで、カテゴリごとに売上金額に応じた順位付けを行います。

---

### 3.3 累計売上の算出 (ウィンドウ関数 SUM OVER)
> **問題**: 日別の売上と、年初からの累積売上推移を計算する。  
> [🔙 問題に戻る](../practice_queries.md#33-累計売上の算出-ウィンドウ関数-sum-over)

#### 模範解答
```sql
WITH daily_sales AS (
    SELECT 
        date(order_date) AS sale_date,
        SUM(total_amount) AS daily_amount
    FROM orders
    WHERE status IN ('paid', 'shipped')
    GROUP BY date(order_date)
)
SELECT 
    sale_date,
    daily_amount,
    SUM(daily_amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_sales
    FROM daily_sales
ORDER BY sale_date ASC;
```

#### 解説
- まず日別の売上合計テーブルを CTE で作成します。
- `SUM(daily_amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` によって、最初の日から現在行までの累積和を算出しています。
