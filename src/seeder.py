import os
import csv
from datetime import datetime, date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import engine, Base, SessionLocal
from src.models import (
    User, Category, Supplier, Product, Coupon, Order, OrderItem, Payment, Review
)

SEEDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seeds")

def parse_val(val: str, target_type: str = "str") -> Any:
    val = val.strip()
    if val == "":
        return None
    if target_type == "int":
        return int(val)
    elif target_type == "float":
        return float(val)
    elif target_type == "bool":
        return val in ("1", "true", "True", "TRUE")
    elif target_type == "date":
        return datetime.strptime(val, "%Y-%m-%d").date()
    elif target_type == "datetime":
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
    return val

def load_csv(filename: str) -> List[Dict[str, str]]:
    filepath = os.path.join(SEEDS_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Seed file not found: {filepath}")
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def seed_database():
    """データベースのテーブルを初期化し、CSVからシードデータを投入する"""
    print(">> [1/3] 既存テーブルを削除して新規作成中...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(">> テーブル作成完了。")

    session: Session = SessionLocal()
    try:
        print(">> [2/3] seeds/*.csv からデータ読み込み・投入中...")

        # 1. Users
        users_data = load_csv("users.csv")
        for row in users_data:
            session.add(User(
                id=parse_val(row["id"], "int"),
                name=row["name"],
                email=row["email"],
                gender=parse_val(row["gender"]),
                birth_date=parse_val(row["birth_date"], "date"),
                prefecture=parse_val(row["prefecture"]),
                is_active=parse_val(row["is_active"], "bool"),
                registered_at=parse_val(row["registered_at"], "datetime")
            ))
        session.flush()

        # 2. Categories
        categories_data = load_csv("categories.csv")
        for row in categories_data:
            session.add(Category(
                id=parse_val(row["id"], "int"),
                name=row["name"],
                parent_id=parse_val(row["parent_id"], "int")
            ))
        session.flush()

        # 3. Suppliers
        suppliers_data = load_csv("suppliers.csv")
        for row in suppliers_data:
            session.add(Supplier(
                id=parse_val(row["id"], "int"),
                name=row["name"],
                contact_email=parse_val(row["contact_email"]),
                country=row["country"]
            ))
        session.flush()

        # 4. Coupons
        coupons_data = load_csv("coupons.csv")
        for row in coupons_data:
            session.add(Coupon(
                id=parse_val(row["id"], "int"),
                code=row["code"],
                discount_amount=parse_val(row["discount_amount"], "int"),
                discount_rate=parse_val(row["discount_rate"], "float"),
                min_order_amount=parse_val(row["min_order_amount"], "int") or 0,
                valid_from=parse_val(row["valid_from"], "datetime"),
                valid_to=parse_val(row["valid_to"], "datetime")
            ))
        session.flush()

        # 5. Products
        products_data = load_csv("products.csv")
        for row in products_data:
            session.add(Product(
                id=parse_val(row["id"], "int"),
                category_id=parse_val(row["category_id"], "int"),
                supplier_id=parse_val(row["supplier_id"], "int"),
                name=row["name"],
                price=parse_val(row["price"], "int"),
                cost_price=parse_val(row["cost_price"], "int"),
                stock_quantity=parse_val(row["stock_quantity"], "int"),
                created_at=parse_val(row["created_at"], "datetime")
            ))
        session.flush()

        # 6. Orders
        orders_data = load_csv("orders.csv")
        for row in orders_data:
            session.add(Order(
                id=parse_val(row["id"], "int"),
                user_id=parse_val(row["user_id"], "int"),
                coupon_id=parse_val(row["coupon_id"], "int"),
                order_date=parse_val(row["order_date"], "datetime"),
                status=row["status"],
                shipping_fee=parse_val(row["shipping_fee"], "int") or 0,
                total_amount=parse_val(row["total_amount"], "int")
            ))
        session.flush()

        # 7. OrderItems
        order_items_data = load_csv("order_items.csv")
        for row in order_items_data:
            session.add(OrderItem(
                id=parse_val(row["id"], "int"),
                order_id=parse_val(row["order_id"], "int"),
                product_id=parse_val(row["product_id"], "int"),
                quantity=parse_val(row["quantity"], "int"),
                unit_price=parse_val(row["unit_price"], "int")
            ))
        session.flush()

        # 8. Payments
        payments_data = load_csv("payments.csv")
        for row in payments_data:
            session.add(Payment(
                id=parse_val(row["id"], "int"),
                order_id=parse_val(row["order_id"], "int"),
                payment_method=row["payment_method"],
                amount=parse_val(row["amount"], "int"),
                payment_status=row["payment_status"],
                paid_at=parse_val(row["paid_at"], "datetime")
            ))
        session.flush()

        # 9. Reviews
        reviews_data = load_csv("reviews.csv")
        for row in reviews_data:
            session.add(Review(
                id=parse_val(row["id"], "int"),
                user_id=parse_val(row["user_id"], "int"),
                product_id=parse_val(row["product_id"], "int"),
                rating=parse_val(row["rating"], "int"),
                comment=parse_val(row["comment"]),
                created_at=parse_val(row["created_at"], "datetime")
            ))
        session.flush()

        session.commit()
        print(">> [3/3] 全シードデータの登録が完了しました！")

        # 登録件数の確認表示
        table_counts = {
            "users": session.query(User).count(),
            "categories": session.query(Category).count(),
            "suppliers": session.query(Supplier).count(),
            "coupons": session.query(Coupon).count(),
            "products": session.query(Product).count(),
            "orders": session.query(Order).count(),
            "order_items": session.query(OrderItem).count(),
            "payments": session.query(Payment).count(),
            "reviews": session.query(Review).count(),
        }
        print("\n=== 登録テーブルとレコード件数 ===")
        for table, count in table_counts.items():
            print(f"- {table:12s}: {count:3d} 件")
        print("===================================\n")

    except Exception as e:
        session.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
