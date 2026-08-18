# SQL実践練習クエリ集

本ドキュメントでは、作成されたECサイトデータベース（`ecommerce.db`）に対して外部ツール（DBeaver, VSCode SQLite Viewer, SQLite CLI等）で実行できる実践的なSQLクエリ例を掲載しています。

---

## 目次
1. [テーブル結合 (JOIN)]( #1-テーブル結合-join)
   - [1.1 INNER JOIN (内部結合)](#11-inner-join-内部結合)
   - [1.2 LEFT JOIN (左外部結合)](#12-left-join-左外部結合)
   - [1.3 RIGHT JOIN (右外部結合)](#13-right-join-右外部結合)
   - [1.4 FULL OUTER JOIN (完全外部結合)](#14-full-outer-join-完全外部結合)
   - [1.5 自己結合 (Self JOIN)](#15-自己結合-self-join)
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

---

### 1.2 LEFT JOIN (左外部結合)
> **お題**: 一度も注文をしたことがない会員（未購入ユーザー）を検出する。

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

> **お題**: レビューがまだ1件も投稿されていない商品一覧を取得する。

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

---

### 1.3 RIGHT JOIN (右外部結合)
> **お題**: 取り扱い商品がまだ登録されていない仕入先（メーカー）を検出する。
> ※ SQLite 3.39.0 以降で対応しています。

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

---

### 1.4 FULL OUTER JOIN (完全外部結合)
> **お題**: 「仕入先未設定の商品」および「商品が登録されていない仕入先」を両方網羅して取得する。
> ※ SQLite 3.39.0 以降で対応しています。

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

---

### 1.5 自己結合 (Self JOIN)
> **お題**: カテゴリテーブルを自己結合して、子カテゴリ名と親カテゴリ名を並べて表示する。

```sql
SELECT 
    child.id AS sub_category_id,
    child.name AS sub_category_name,
    COALESCE(parent.name, '（最上位カテゴリ）') AS parent_category_name
FROM categories child
LEFT JOIN categories parent ON child.parent_id = parent.id
ORDER BY parent.id, child.id;
```

---

## 2. 集計と絞り込み (GROUP BY / HAVING)

### 2.1 都道府県別の会員数と購入総額
> **お題**: 都道府県ごとの会員数と、その都道府県の会員による総購入金額・注文件数を集計する。

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

---

### 2.2 複数回購入しているリピーター会員の抽出 (HAVING)
> **お題**: 注文回数が2回以上で、合計購入額が20,000円以上の優良リピーターを抽出する。

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

---

### 2.3 平均評価が4.0以上の高評価商品の抽出 (HAVING)
> **お題**: レビューが2件以上投稿されており、かつ平均評価（星）が4.0以上の商品を取得する。

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

---

### 2.4 月別売上高と注文件数の集計
> **お題**: 注文年月（YYYY-MM）ごとに、注文件数・売上合計・平均客単価を集計する。

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

---

## 3. サブクエリ・ウィンドウ関数 (応用)

### 3.1 全体平均より高い商品のみ抽出 (サブクエリ)
> **お題**: 全商品の平均販売価格よりも高い商品一覧と、平均との価格差を取得する。

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

---

### 3.2 カテゴリごとの売上ランキング (ウィンドウ関数 RANK)
> **お題**: カテゴリごとに、商品の売上数量ランキングを算出する。

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

---

### 3.3 累計売上の算出 (ウィンドウ関数 SUM OVER)
> **お題**: 日別の売上と、年初からの累積売上推移を計算する。

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
