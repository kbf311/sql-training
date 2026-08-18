"""
SQL練習用 ECサイトデータベース初期化スクリプト
実行方法: python main.py
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.seeder import seed_database
from src.database import DB_PATH

def main():
    print("==========================================================")
    print("  SQL Training - ECサイト データベースセットアップ")
    print("==========================================================")
    print(f"対象データベースファイル: {DB_PATH}\n")
    
    seed_database()
    
    print("セットアップが正常に完了しました！")
    print(f" -> {DB_PATH}")
    print("==========================================================")

if __name__ == "__main__":
    main()
