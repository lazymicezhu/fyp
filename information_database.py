#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
独立信息库管理系统
支持JSON文件存储、GUI数据输入、导入导出等功能
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Optional

class InformationDatabase:
    """信息库管理类"""
    
    def __init__(self, data_file: str = "information_database.json"):
        """
        初始化信息库
        
        Args:
            data_file: 数据文件路径
        """
        self.data_file = data_file
        self.data = []
        self.load_data()
    
    def load_data(self):
        """从JSON文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"成功加载 {len(self.data)} 条数据")
            else:
                print("数据文件不存在，创建新的信息库")
                self.data = []
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.data = []
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"成功保存 {len(self.data)} 条数据")
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def add_entry(self, title: str, content: str, url: str, tags: List[str] = None) -> bool:
        """
        添加信息条目
        
        Args:
            title: 标题
            content: 内容
            url: URL
            tags: 标签列表
            
        Returns:
            是否添加成功
        """
        if not title.strip() or not content.strip():
            print("标题和内容不能为空")
            return False
        
        if tags is None:
            tags = []
        
        entry = {
            "id": len(self.data) + 1,
            "title": title.strip(),
            "content": content.strip(),
            "url": url.strip(),
            "tags": [tag.strip() for tag in tags if tag.strip()],
            "searchable_text": f"{title} {content} {' '.join(tags)}".lower(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.data.append(entry)
        return True
    
    def update_entry(self, entry_id: int, title: str = None, content: str = None, 
                    url: str = None, tags: List[str] = None) -> bool:
        """
        更新信息条目
        
        Args:
            entry_id: 条目ID
            title: 新标题
            content: 新内容
            url: 新URL
            tags: 新标签列表
            
        Returns:
            是否更新成功
        """
        for entry in self.data:
            if entry["id"] == entry_id:
                if title is not None:
                    entry["title"] = title.strip()
                if content is not None:
                    entry["content"] = content.strip()
                if url is not None:
                    entry["url"] = url.strip()
                if tags is not None:
                    entry["tags"] = [tag.strip() for tag in tags if tag.strip()]
                
                # 更新搜索文本和时间
                entry["searchable_text"] = f"{entry['title']} {entry['content']} {' '.join(entry['tags'])}".lower()
                entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return True
        
        print(f"未找到ID为 {entry_id} 的条目")
        return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        删除信息条目
        
        Args:
            entry_id: 条目ID
            
        Returns:
            是否删除成功
        """
        for i, entry in enumerate(self.data):
            if entry["id"] == entry_id:
                del self.data[i]
                return True
        
        print(f"未找到ID为 {entry_id} 的条目")
        return False
    
    def search(self, query: str) -> List[Dict]:
        """
        搜索信息库
        
        Args:
            query: 搜索关键词
            
        Returns:
            搜索结果列表
        """
        if not query.strip():
            return []
        
        query = query.lower()
        results = []
        
        for entry in self.data:
            # 计算匹配度
            score = 0
            
            # 标题完全匹配
            if query in entry["title"].lower():
                score += 10
            
            # 内容匹配
            content_matches = len(re.findall(query, entry["content"].lower()))
            score += content_matches * 2
            
            # 标签匹配
            for tag in entry["tags"]:
                if query in tag.lower():
                    score += 5
            
            # 可搜索文本匹配
            text_matches = len(re.findall(query, entry["searchable_text"]))
            score += text_matches
            
            if score > 0:
                results.append((entry, score))
        
        # 按匹配度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results]
    
    def get_all_entries(self) -> List[Dict]:
        """获取所有条目"""
        return self.data.copy()
    
    def get_entry_by_id(self, entry_id: int) -> Optional[Dict]:
        """根据ID获取条目"""
        for entry in self.data:
            if entry["id"] == entry_id:
                return entry
        return None
    
    def export_to_json(self, filename: str = None) -> bool:
        """
        导出数据到JSON文件
        
        Args:
            filename: 导出文件名
            
        Returns:
            是否导出成功
        """
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"成功导出到 {filename}")
            return True
        except Exception as e:
            print(f"导出失败: {e}")
            return False
    
    def import_from_json(self, filename: str) -> bool:
        """
        从JSON文件导入数据
        
        Args:
            filename: 导入文件名
            
        Returns:
            是否导入成功
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            if isinstance(imported_data, list):
                # 重新分配ID
                for i, entry in enumerate(imported_data):
                    entry["id"] = len(self.data) + i + 1
                    entry["searchable_text"] = f"{entry['title']} {entry['content']} {' '.join(entry.get('tags', []))}".lower()
                    if "created_at" not in entry:
                        entry["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.data.extend(imported_data)
                print(f"成功导入 {len(imported_data)} 条数据")
                return True
            else:
                print("导入文件格式错误")
                return False
        except Exception as e:
            print(f"导入失败: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """获取信息库统计信息"""
        total_entries = len(self.data)
        total_tags = set()
        for entry in self.data:
            total_tags.update(entry.get("tags", []))
        
        return {
            "total_entries": total_entries,
            "total_tags": len(total_tags),
            "tags_list": sorted(list(total_tags)),
            "data_file": self.data_file,
            "file_size": os.path.getsize(self.data_file) if os.path.exists(self.data_file) else 0
        }

if __name__ == "__main__":
    # 测试信息库功能
    db = InformationDatabase()
    
    # 添加测试数据
    db.add_entry(
        title="测试条目",
        content="这是一个测试条目，用于验证信息库功能。",
        url="test.html",
        tags=["测试", "示例"]
    )
    
    # 保存数据
    db.save_data()
    
    # 搜索测试
    results = db.search("测试")
    print(f"搜索结果: {len(results)} 条")
    
    # 显示统计信息
    stats = db.get_statistics()
    print(f"统计信息: {stats}")
