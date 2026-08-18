from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Integer, String, Float, DateTime, Date, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class User(Base):
    """会員テーブル"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True) # 'male', 'female', 'other'
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    prefecture: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")


class Category(Base):
    """商品カテゴリテーブル（自己参照階層構造）"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    parent: Mapped[Optional["Category"]] = relationship("Category", remote_side=[id], backref="children")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")


class Supplier(Base):
    """仕入先テーブル"""
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(50), default="Japan", nullable=False)

    # Relationships
    products: Mapped[List["Product"]] = relationship("Product", back_populates="supplier")


class Product(Base):
    """商品テーブル"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False) # 販売価格（税込）
    cost_price: Mapped[int] = mapped_column(Integer, nullable=False) # 仕入原価
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")
    supplier: Mapped[Optional["Supplier"]] = relationship("Supplier", back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="product")


class Coupon(Base):
    """クーポンテーブル"""
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    discount_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True) # 固定値引額
    discount_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # 割引率 (例: 0.10 for 10%OFF)
    min_order_amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False) # 適用最小注文金額
    valid_from: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    valid_to: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="coupon")


class Order(Base):
    """注文テーブル"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coupon_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("coupons.id", ondelete="SET NULL"), nullable=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False) # pending, paid, shipped, cancelled, refunded
    shipping_fee: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    coupon: Mapped[Optional["Coupon"]] = relationship("Coupon", back_populates="orders")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment: Mapped[Optional["Payment"]] = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    """注文明細テーブル"""
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False) # 注文時点の単価

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")


class Payment(Base):
    """決済テーブル"""
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False) # credit_card, bank_transfer, cod, paypay, convenience_store
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False) # completed, pending, failed
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payment")


class Review(Base):
    """商品レビューテーブル"""
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False) # 1 ~ 5
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")
