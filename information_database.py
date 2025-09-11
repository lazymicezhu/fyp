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
    """
    信息库管理类
    提供完整的信息库管理功能，包括数据的增删改查、搜索、导入导出等
    支持多种内容类型和元数据，使用JSON格式进行数据持久化
    """
    
    def __init__(self, data_file: str = "information_database.json"):
        """
        初始化信息库
        设置数据文件路径，初始化数据列表，加载现有数据
        
        Args:
            data_file: 数据文件路径，默认为"information_database.json"
        """
        # 设置数据文件路径
        self.data_file = data_file
        # 初始化数据列表，用于存储所有信息条目
        self.data = []
        # 从文件加载现有数据
        self.load_data()
    
    def load_data(self):
        """
        从JSON文件加载数据
        如果文件存在则读取数据，否则创建空的数据列表
        """
        try:
            # 检查数据文件是否存在
            if os.path.exists(self.data_file):
                # 如果文件存在，打开并读取JSON数据
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                # 打印成功加载的数据条数
                print(f"成功加载 {len(self.data)} 条数据")
            else:
                # 如果文件不存在，创建新的空数据列表
                print("数据文件不存在，创建新的信息库")
                self.data = []
        except Exception as e:
            # 如果加载过程中出现错误，打印错误信息并创建空数据列表
            print(f"加载数据失败: {e}")
            self.data = []
    
    def save_data(self):
        """
        保存数据到JSON文件
        将当前数据列表保存到指定的JSON文件中
        """
        try:
            # 打开数据文件进行写入操作
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # 将数据列表转换为JSON格式并写入文件
                # ensure_ascii=False: 允许中文字符正常显示
                # indent=2: 设置缩进为2个空格，使JSON文件更易读
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            # 打印成功保存的数据条数
            print(f"成功保存 {len(self.data)} 条数据")
            return True
        except Exception as e:
            # 如果保存过程中出现错误，打印错误信息并返回False
            print(f"保存数据失败: {e}")
            return False
    
    def add_entry(self, title: str, content: str, url: str, tags: List[str] = None, 
                  content_type: str = "article", metadata: dict = None) -> bool:
        """
        添加信息条目
        创建新的信息条目并添加到数据库中
        
        Args:
            title: 标题
            content: 内容
            url: URL
            tags: 标签列表
            content_type: 内容类型 (article, link, image, video, code, news, tutorial, tool)
            metadata: 额外元数据
            
        Returns:
            是否添加成功
        """
        # 验证标题不能为空
        if not title.strip():
            print("标题不能为空")
            return False
        
        # 验证文章类型的内容不能为空
        if content_type == "article" and not content.strip():
            print("文章类型的内容不能为空")
            return False
        
        # 如果标签为空，初始化为空列表
        if tags is None:
            tags = []
        
        # 如果元数据为空，初始化为空字典
        if metadata is None:
            metadata = {}
        
        # 根据内容类型生成不同的搜索文本
        # 将标题转换为小写并添加到搜索部分
        searchable_parts = [title.lower()]
        # 如果内容不为空，将内容转换为小写并添加
        if content.strip():
            searchable_parts.append(content.lower())
        # 将所有标签转换为小写并添加
        searchable_parts.extend([tag.lower() for tag in tags if tag.strip()])
        
        # 添加类型特定的搜索内容
        # 如果元数据中包含内容类型相关的信息，也添加到搜索文本中
        if content_type in metadata:
            searchable_parts.append(str(metadata[content_type]).lower())
        
        # 创建新的信息条目字典
        # 包含所有必要的字段和元数据
        entry = {
            "id": len(self.data) + 1,  # 自动生成唯一ID
            "title": title.strip(),      # 去除首尾空格的标题
            "content": content.strip(),  # 去除首尾空格的内容
            "url": url.strip(),          # 去除首尾空格的URL
            "tags": [tag.strip() for tag in tags if tag.strip()],  # 清理标签列表
            "content_type": content_type,  # 内容类型
            "metadata": metadata,        # 元数据字典
            "searchable_text": " ".join(searchable_parts),  # 合并搜索文本
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 创建时间
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # 更新时间
        }
        
        # 将新条目添加到数据列表中
        self.data.append(entry)
        return True
    
    def update_entry(self, entry_id: int, title: str = None, content: str = None, 
                    url: str = None, tags: List[str] = None, content_type: str = None,
                    metadata: dict = None) -> bool:
        """
        更新信息条目
        根据条目ID查找并更新指定的信息条目
        
        Args:
            entry_id: 条目ID
            title: 新标题
            content: 新内容
            url: 新URL
            tags: 新标签列表
            content_type: 新内容类型
            metadata: 新元数据
            
        Returns:
            是否更新成功
        """
        # 遍历数据列表，查找指定ID的条目
        for entry in self.data:
            if entry["id"] == entry_id:
                # 如果提供了新标题，更新标题
                if title is not None:
                    entry["title"] = title.strip()
                # 如果提供了新内容，更新内容
                if content is not None:
                    entry["content"] = content.strip()
                # 如果提供了新URL，更新URL
                if url is not None:
                    entry["url"] = url.strip()
                # 如果提供了新标签，更新标签列表
                if tags is not None:
                    entry["tags"] = [tag.strip() for tag in tags if tag.strip()]
                # 如果提供了新内容类型，更新内容类型
                if content_type is not None:
                    entry["content_type"] = content_type
                # 如果提供了新元数据，更新元数据
                if metadata is not None:
                    entry["metadata"] = metadata
                
                # 更新搜索文本和时间戳
                # 重新生成搜索文本，包含更新后的内容
                searchable_parts = [entry["title"].lower()]
                # 如果内容不为空，添加到搜索文本中
                if entry["content"].strip():
                    searchable_parts.append(entry["content"].lower())
                # 将所有标签添加到搜索文本中
                searchable_parts.extend([tag.lower() for tag in entry["tags"] if tag.strip()])
                
                # 添加类型特定的搜索内容
                # 如果元数据中包含内容类型相关的信息，也添加到搜索文本中
                if entry["content_type"] in entry.get("metadata", {}):
                    searchable_parts.append(str(entry["metadata"][entry["content_type"]]).lower())
                
                # 更新搜索文本和更新时间
                entry["searchable_text"] = " ".join(searchable_parts)
                entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return True
        
        # 如果未找到指定ID的条目，打印错误信息
        print(f"未找到ID为 {entry_id} 的条目")
        return False
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        删除信息条目
        根据条目ID查找并删除指定的信息条目
        
        Args:
            entry_id: 条目ID
            
        Returns:
            是否删除成功
        """
        # 遍历数据列表，查找指定ID的条目
        for i, entry in enumerate(self.data):
            if entry["id"] == entry_id:
                # 找到指定条目，从列表中删除
                del self.data[i]
                return True
        
        # 如果未找到指定ID的条目，打印错误信息
        print(f"未找到ID为 {entry_id} 的条目")
        return False
    
    def search(self, query: str) -> List[Dict]:
        """
        搜索信息库
        使用模糊搜索算法在信息库中查找匹配的条目
        
        Args:
            query: 搜索关键词
            
        Returns:
            搜索结果列表，按匹配度排序
        """
        # 如果查询为空，返回空列表
        if not query.strip():
            return []
        
        # 将查询转换为小写，便于匹配
        query = query.lower()
        results = []
        
        # 遍历所有数据条目，计算匹配度
        for entry in self.data:
            # 初始化匹配度分数
            score = 0
            
            # 标题完全匹配：如果查询词在标题中，增加10分
            if query in entry["title"].lower():
                score += 10
            
            # 内容匹配：如果查询词在内容中，增加5分
            # 内容匹配：使用正则表达式计算内容中查询词的出现次数
            content_matches = len(re.findall(query, entry["content"].lower()))
            # 每个匹配增加2分
            score += content_matches * 2
            
            # 标签匹配：如果查询词在标签中，增加5分
            for tag in entry["tags"]:
                if query in tag.lower():
                    score += 5
            
            # 可搜索文本匹配：在合并的搜索文本中查找匹配
            text_matches = len(re.findall(query, entry["searchable_text"]))
            # 每个匹配增加1分
            score += text_matches
            
            # 如果匹配度大于0，将条目和分数添加到结果中
            if score > 0:
                results.append((entry, score))
        
        # 按匹配度分数降序排序，返回条目列表
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results]
    
    def get_all_entries(self) -> List[Dict]:
        """
        获取所有条目
        返回数据库中所有条目的副本
        
        Returns:
            所有条目的列表
        """
        return self.data.copy()
    
    def get_entry_by_id(self, entry_id: int) -> Optional[Dict]:
        """
        根据ID获取条目
        在数据库中查找指定ID的条目
        
        Args:
            entry_id: 条目ID
            
        Returns:
            找到的条目，如果未找到则返回None
        """
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
    
    def get_content_types(self) -> Dict[str, int]:
        """获取内容类型统计"""
        type_count = {}
        for entry in self.data:
            content_type = entry.get("content_type", "article")
            type_count[content_type] = type_count.get(content_type, 0) + 1
        return type_count
    
    def get_entries_by_type(self, content_type: str) -> List[Dict]:
        """根据内容类型获取条目"""
        return [entry for entry in self.data if entry.get("content_type") == content_type]
    
    def get_content_type_info(self) -> Dict[str, str]:
        """获取内容类型说明"""
        return {
            "article": "文章 - 长文本内容",
            "link": "链接 - 外部网站链接",
            "image": "图片 - 图片资源",
            "video": "视频 - 视频资源",
            "code": "代码 - 代码片段",
            "news": "新闻 - 新闻摘要",
            "tutorial": "教程 - 分步骤教程",
            "tool": "工具 - 工具推荐"
        }
    
    def get_statistics(self) -> Dict:
        """获取信息库统计信息"""
        total_entries = len(self.data)
        total_tags = set()
        content_types = self.get_content_types()
        
        for entry in self.data:
            total_tags.update(entry.get("tags", []))
        
        return {
            "total_entries": total_entries,
            "total_tags": len(total_tags),
            "tags_list": sorted(list(total_tags)),
            "content_types": content_types,
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
