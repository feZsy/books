import os
import json

def generate_book_json():
    base_dir = 'books'
    book_tree = {}

    # 支持的书籍格式
    book_exts = ('.pdf', '.epub', '.mobi')

    for root, dirs, files in os.walk(base_dir):
        category = os.path.relpath(root, base_dir)
        if category == '.': continue
        
        books_in_cat = []
        # 先找出所有的书籍文件
        book_files = [f for f in files if f.lower().endswith(book_exts)]
        
        for b_file in book_files:
            name_without_ext = os.path.splitext(b_file)[0]
            summary = ""
            
            # 寻找同名的摘要文件 (.txt 或 .md)
            for s_ext in ['.txt', '.md']:
                s_path = os.path.join(root, name_without_ext + s_ext)
                if os.path.exists(s_path):
                    with open(s_path, 'r', encoding='utf-8') as f:
                        summary = f.read().strip()
                    break
            
            books_in_cat.append({
                "title": name_without_ext,
                "fileName": b_file,
                "summary": summary if summary else "暂无概要..."
            })

        if books_in_cat:
            book_tree[category] = books_in_cat

    with open('books_data.json', 'w', encoding='utf-8') as f:
        json.dump(book_tree, f, ensure_ascii=False, indent=4)
    
    print(f"✅ 索引同步完成！共发现 {sum(len(v) for v in book_tree.values())} 本书籍。")

if __name__ == "__main__":
    generate_book_json()