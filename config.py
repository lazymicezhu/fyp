#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息库系统配置管理模块
统一管理系统配置项，避免硬编码，提高可维护性
支持配置文件自动加载和运行时配置修改
"""

import os
import platform
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class WindowConfig:
    """
    窗口配置类
    定义各个窗口的基本配置参数
    """
    width: int
    height: int
    min_width: int
    min_height: int
    resizable: bool = True
    center: bool = True

@dataclass  
class FontConfig:
    """
    字体配置类
    定义不同平台下的字体设置
    """
    family: str
    size: int
    bold: bool = False

class Config:
    """
    配置管理类
    统一管理系统的各种配置项
    支持从配置文件加载和保存配置
    采用单例模式确保配置的一致性
    """
    
    _instance: Optional['Config'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'Config':
        """
        单例模式实现
        确保整个应用只有一个配置管理实例
        
        Returns:
            Config: 配置管理实例
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        初始化配置管理器
        如果已经初始化则跳过，避免重复初始化
        加载默认配置和用户配置文件
        """
        if Config._initialized:
            return
        Config._initialized = True
        
        # 配置文件路径
        self.config_file = "app_config.json"
        
        # 初始化默认配置
        self._init_default_config()
        
        # 加载用户配置文件（如果存在）
        self._load_user_config()
    
    def _init_default_config(self):
        """
        初始化默认配置
        定义系统的默认配置项，包括窗口、字体、数据库等设置
        根据不同操作系统设置合适的默认值
        """
        
        # 数据库配置
        self.DATABASE = {
            "file": "information_database.json",           # 数据文件路径
            "backup_dir": "backups",                       # 备份目录
            "auto_backup": True,                           # 是否自动备份
            "backup_interval": 3600,                       # 备份间隔(秒)
            "max_backups": 10                              # 最大备份文件数
        }
        
        # 搜索配置
        self.SEARCH = {
            "history_file": "search_history.json",        # 搜索历史文件
            "max_history": 100,                            # 最大历史记录数
            "fuzzy_threshold": 0.6,                        # 模糊搜索阈值
            "highlight_color": "#ffff00",                  # 搜索结果高亮颜色
            "results_per_page": 10                         # 每页搜索结果数
        }
        
        # 窗口配置
        self.WINDOWS = {
            "launcher": WindowConfig(
                width=500, height=630,
                min_width=400, min_height=500,
                resizable=True, center=True
            ),
            "search": WindowConfig(
                width=1024, height=768,
                min_width=800, min_height=600,
                resizable=True, center=True
            ),
            "data_manager": WindowConfig(
                width=1200, height=800,
                min_width=1000, min_height=700,
                resizable=True, center=True
            ),
            "help": WindowConfig(
                width=600, height=500,
                min_width=500, min_height=400,
                resizable=True, center=True
            )
        }
        
        # 字体配置
        self.FONTS = self._get_platform_fonts()
        
        # UI主题配置
        self.THEME = {
            "background": "#f5f5f5",                       # 背景色
            "foreground": "#333333",                       # 前景色（文字）
            "accent": "#4285f4",                          # 强调色（按钮等）
            "secondary": "#34a853",                       # 次要色
            "warning": "#fbbc04",                         # 警告色
            "danger": "#ea4335",                          # 危险色（删除等）
            "border": "#e0e0e0",                          # 边框色
            "hover": "#e8f0fe"                            # 悬停色
        }
        
        # 界面布局配置
        self.LAYOUT = {
            "padding": 20,                                # 默认内边距
            "margin": 10,                                 # 默认外边距
            "button_height": 40,                          # 按钮高度
            "input_height": 35,                           # 输入框高度
            "border_radius": 4,                           # 圆角半径
            "animation_duration": 200                     # 动画持续时间(毫秒)
        }
        
        # 性能配置
        self.PERFORMANCE = {
            "search_delay": 300,                          # 搜索延迟(毫秒)
            "scroll_batch_size": 50,                      # 滚动加载批次大小
            "image_cache_size": 100,                      # 图片缓存大小
            "lazy_load_threshold": 20                     # 懒加载阈值
        }
        
        # 日志配置
        self.LOGGING = {
            "level": "INFO",                              # 日志级别
            "file": "app.log",                           # 日志文件
            "max_size": 10 * 1024 * 1024,               # 最大文件大小(10MB)
            "backup_count": 5,                           # 备份文件数量
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    
    def _get_platform_fonts(self) -> Dict[str, FontConfig]:
        """
        获取平台相关的字体配置
        根据不同操作系统选择最适合的中文字体
        
        Returns:
            Dict[str, FontConfig]: 字体配置字典
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows系统使用微软雅黑字体系列
            return {
                "default": FontConfig("Microsoft YaHei", 11),
                "title": FontConfig("Microsoft YaHei", 16, bold=True),
                "subtitle": FontConfig("Microsoft YaHei", 12),
                "button": FontConfig("Microsoft YaHei", 10),
                "input": FontConfig("Microsoft YaHei", 10),
                "code": FontConfig("Consolas", 10)
            }
        elif system == "Darwin":
            # macOS系统使用苹方字体系列
            return {
                "default": FontConfig("PingFang SC", 12),
                "title": FontConfig("PingFang SC", 17, bold=True),
                "subtitle": FontConfig("PingFang SC", 13),
                "button": FontConfig("PingFang SC", 11),
                "input": FontConfig("PingFang SC", 11),
                "code": FontConfig("Menlo", 11)
            }
        else:
            # Linux等其他系统使用通用字体
            return {
                "default": FontConfig("Arial", 11),
                "title": FontConfig("Arial", 16, bold=True),
                "subtitle": FontConfig("Arial", 12),
                "button": FontConfig("Arial", 10),
                "input": FontConfig("Arial", 10),
                "code": FontConfig("monospace", 10)
            }
    
    def _load_user_config(self):
        """
        加载用户配置文件
        如果用户配置文件存在，则合并用户配置到默认配置中
        支持部分配置覆盖，保持配置的灵活性
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # 合并用户配置到当前配置
                self._merge_config(user_config)
                print(f"已加载用户配置文件: {self.config_file}")
            else:
                print("未找到用户配置文件，使用默认配置")
        except Exception as e:
            print(f"加载用户配置失败: {e}，使用默认配置")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """
        合并用户配置到当前配置
        递归合并配置项，支持嵌套配置的部分更新
        
        Args:
            user_config: 用户配置字典
        """
        def merge_dict(target: Dict[str, Any], source: Dict[str, Any]):
            """递归合并字典"""
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    merge_dict(target[key], value)
                else:
                    target[key] = value
        
        # 合并各个配置项
        for section, values in user_config.items():
            if hasattr(self, section) and isinstance(getattr(self, section), dict):
                merge_dict(getattr(self, section), values)
            else:
                setattr(self, section, values)
    
    def save_config(self):
        """
        保存当前配置到配置文件
        将运行时的配置更改持久化到文件中
        自动创建配置目录，处理保存过程中的异常
        """
        try:
            # 准备要保存的配置数据
            config_data = {
                "DATABASE": self.DATABASE,
                "SEARCH": self.SEARCH,
                "THEME": self.THEME,
                "LAYOUT": self.LAYOUT,
                "PERFORMANCE": self.PERFORMANCE,
                "LOGGING": self.LOGGING
            }
            
            # 保存配置到文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"配置已保存到: {self.config_file}")
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get_window_config(self, window_name: str) -> WindowConfig:
        """
        获取指定窗口的配置
        如果窗口配置不存在，返回默认的启动器窗口配置
        
        Args:
            window_name: 窗口名称
            
        Returns:
            WindowConfig: 窗口配置对象
        """
        return self.WINDOWS.get(window_name, self.WINDOWS["launcher"])
    
    def get_font_config(self, font_type: str = "default") -> FontConfig:
        """
        获取指定类型的字体配置
        如果字体类型不存在，返回默认字体配置
        
        Args:
            font_type: 字体类型 (default, title, subtitle, button, input, code)
            
        Returns:
            FontConfig: 字体配置对象
        """
        return self.FONTS.get(font_type, self.FONTS["default"])
    
    def get_font_tuple(self, font_type: str = "default") -> tuple:
        """
        获取字体元组格式
        用于Tkinter的font参数，返回(family, size, style)格式
        
        Args:
            font_type: 字体类型
            
        Returns:
            tuple: (字体族, 大小, 样式)
        """
        font = self.get_font_config(font_type)
        style = "bold" if font.bold else "normal"
        return (font.family, font.size, style)
    
    def update_config(self, section: str, key: str, value: Any) -> bool:
        """
        更新配置项
        支持运行时修改配置，并可选择是否立即保存到文件
        
        Args:
            section: 配置区段名称
            key: 配置键名
            value: 新的配置值
            
        Returns:
            bool: 是否更新成功
        """
        try:
            if hasattr(self, section):
                section_config = getattr(self, section)
                if isinstance(section_config, dict):
                    section_config[key] = value
                    return True
            return False
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False
    
    def reset_to_defaults(self):
        """
        重置配置到默认值
        清除所有用户自定义配置，恢复到系统默认状态
        """
        self._init_default_config()
        print("配置已重置为默认值")

# 创建全局配置实例
# 使用单例模式确保整个应用共享同一个配置对象
config = Config()