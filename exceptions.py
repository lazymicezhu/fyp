#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息库系统异常处理模块
定义系统中所有可能出现的异常类型
提供统一的异常处理机制和错误报告功能
"""

import logging
import traceback
from datetime import datetime
from typing import Optional, Any, Dict
from functools import wraps

class BaseInfoError(Exception):
    """
    信息库系统基础异常类
    所有自定义异常的父类，提供统一的异常处理接口
    包含错误代码、详细信息和时间戳等基本信息
    """
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        """
        初始化基础异常
        
        Args:
            message: 错误消息
            error_code: 错误代码，用于程序化处理
            details: 详细信息字典，用于调试和日志记录
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换异常信息为字典格式
        用于日志记录和错误报告
        
        Returns:
            Dict[str, Any]: 异常信息字典
        """
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "traceback": traceback.format_exc()
        }

class DatabaseError(BaseInfoError):
    """
    数据库相关异常
    包括数据文件读写、JSON解析、数据格式等错误
    """
    
    def __init__(self, message: str, operation: str = None, file_path: str = None):
        """
        初始化数据库异常
        
        Args:
            message: 错误消息
            operation: 出错的操作类型（load, save, parse等）
            file_path: 相关文件路径
        """
        details = {
            "operation": operation,
            "file_path": file_path
        }
        super().__init__(message, "DB_ERROR", details)

class ValidationError(BaseInfoError):
    """
    数据验证异常
    用于输入数据格式、必填字段、数据完整性等验证错误
    """
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        """
        初始化验证异常
        
        Args:
            message: 错误消息
            field: 出错的字段名
            value: 出错的字段值
        """
        details = {
            "field": field,
            "value": str(value) if value is not None else None
        }
        super().__init__(message, "VALIDATION_ERROR", details)

class SearchError(BaseInfoError):
    """
    搜索功能异常
    包括搜索参数错误、搜索引擎故障、结果处理错误等
    """
    
    def __init__(self, message: str, query: str = None, search_type: str = None):
        """
        初始化搜索异常
        
        Args:
            message: 错误消息
            query: 搜索查询内容
            search_type: 搜索类型（keyword, fuzzy, advanced等）
        """
        details = {
            "query": query,
            "search_type": search_type
        }
        super().__init__(message, "SEARCH_ERROR", details)

class UIError(BaseInfoError):
    """
    用户界面异常
    包括界面初始化、组件创建、事件处理等UI相关错误
    """
    
    def __init__(self, message: str, component: str = None, action: str = None):
        """
        初始化UI异常
        
        Args:
            message: 错误消息
            component: 出错的UI组件名称
            action: 出错的操作类型
        """
        details = {
            "component": component,
            "action": action
        }
        super().__init__(message, "UI_ERROR", details)

class ConfigError(BaseInfoError):
    """
    配置相关异常
    包括配置文件读写、配置项验证、默认值设置等错误
    """
    
    def __init__(self, message: str, config_file: str = None, config_key: str = None):
        """
        初始化配置异常
        
        Args:
            message: 错误消息
            config_file: 配置文件路径
            config_key: 出错的配置项键名
        """
        details = {
            "config_file": config_file,
            "config_key": config_key
        }
        super().__init__(message, "CONFIG_ERROR", details)

class ExportImportError(BaseInfoError):
    """
    导入导出功能异常
    包括文件格式错误、权限问题、数据转换错误等
    """
    
    def __init__(self, message: str, file_path: str = None, operation: str = None):
        """
        初始化导入导出异常
        
        Args:
            message: 错误消息
            file_path: 相关文件路径
            operation: 操作类型（import, export）
        """
        details = {
            "file_path": file_path,
            "operation": operation
        }
        super().__init__(message, "IMPORT_EXPORT_ERROR", details)

def safe_execute(error_type: type = BaseInfoError, 
                default_return: Any = None,
                log_error: bool = True,
                show_user_error: bool = True):
    """
    安全执行装饰器
    为函数提供统一的异常处理和错误恢复机制
    
    Args:
        error_type: 要捕获的异常类型
        default_return: 异常时的默认返回值
        log_error: 是否记录错误日志
        show_user_error: 是否向用户显示错误信息
    
    Returns:
        装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_type as e:
                # 记录错误日志
                if log_error:
                    logging.error(f"函数 {func.__name__} 执行失败: {e.message}", 
                                extra=e.to_dict())
                
                # 向用户显示友好的错误信息（如果需要）
                if show_user_error:
                    error_handler.show_user_error(e)
                
                return default_return
            except Exception as e:
                # 处理未预期的异常
                base_error = BaseInfoError(
                    f"函数 {func.__name__} 发生未知错误: {str(e)}",
                    "UNKNOWN_ERROR",
                    {"function": func.__name__, "args": str(args), "kwargs": str(kwargs)}
                )
                
                if log_error:
                    logging.error(f"未知错误: {str(e)}", extra=base_error.to_dict())
                
                if show_user_error:
                    error_handler.show_user_error(base_error)
                
                return default_return
        return wrapper
    return decorator

class ErrorHandler:
    """
    错误处理器类
    提供统一的错误处理、日志记录和用户通知机制
    支持不同级别的错误处理策略
    """
    
    def __init__(self):
        """
        初始化错误处理器
        设置日志记录器和错误统计
        """
        self.logger = logging.getLogger(__name__)
        self.error_count = {}
        self.last_errors = []
        self.max_last_errors = 50
    
    def handle_error(self, error: BaseInfoError, context: str = None) -> bool:
        """
        处理错误
        根据错误类型和严重程度选择合适的处理策略
        
        Args:
            error: 异常对象
            context: 错误发生的上下文信息
            
        Returns:
            bool: 是否成功处理错误
        """
        try:
            # 记录错误统计
            error_type = error.__class__.__name__
            self.error_count[error_type] = self.error_count.get(error_type, 0) + 1
            
            # 添加到最近错误列表
            error_info = {
                "error": error,
                "context": context,
                "timestamp": datetime.now()
            }
            self.last_errors.append(error_info)
            if len(self.last_errors) > self.max_last_errors:
                self.last_errors.pop(0)
            
            # 记录详细错误日志
            self.logger.error(
                f"错误处理 - 类型: {error_type}, 消息: {error.message}",
                extra={
                    "context": context,
                    "error_details": error.to_dict()
                }
            )
            
            # 根据错误类型决定是否需要用户交互
            if isinstance(error, (ValidationError, UIError)):
                self.show_user_error(error)
            elif isinstance(error, DatabaseError):
                self.show_user_error(error, suggest_backup=True)
            
            return True
            
        except Exception as e:
            # 错误处理器本身出错的情况
            self.logger.critical(f"错误处理器失败: {str(e)}")
            return False
    
    def show_user_error(self, error: BaseInfoError, suggest_backup: bool = False):
        """
        向用户显示错误信息
        根据错误类型显示不同级别的用户提示
        
        Args:
            error: 异常对象
            suggest_backup: 是否建议用户备份数据
        """
        try:
            import tkinter.messagebox as messagebox
            
            # 构建用户友好的错误消息
            user_message = self._format_user_message(error)
            
            if suggest_backup:
                user_message += "\n\n建议立即备份您的数据以避免数据丢失。"
            
            # 根据错误严重程度选择对话框类型
            if isinstance(error, ValidationError):
                messagebox.showwarning("输入错误", user_message)
            elif isinstance(error, DatabaseError):
                messagebox.showerror("数据错误", user_message)
            else:
                messagebox.showerror("系统错误", user_message)
                
        except ImportError:
            # 如果无法导入tkinter（如在测试环境中），使用print输出
            print(f"错误: {error.message}")
        except Exception as e:
            # 如果显示错误信息也失败了，至少记录到日志
            self.logger.error(f"无法显示用户错误: {str(e)}")
    
    def _format_user_message(self, error: BaseInfoError) -> str:
        """
        格式化用户错误消息
        将技术性错误信息转换为用户友好的描述
        
        Args:
            error: 异常对象
            
        Returns:
            str: 格式化后的用户消息
        """
        base_message = error.message
        
        # 根据错误类型添加用户指导信息
        if isinstance(error, ValidationError):
            field = error.details.get("field", "某个字段")
            base_message += f"\n\n请检查 '{field}' 字段的输入格式是否正确。"
        
        elif isinstance(error, DatabaseError):
            operation = error.details.get("operation", "数据操作")
            base_message += f"\n\n{operation} 操作失败，可能是文件权限问题或磁盘空间不足。"
        
        elif isinstance(error, SearchError):
            query = error.details.get("query", "")
            if query:
                base_message += f"\n\n搜索查询: '{query}'"
            base_message += "\n\n请尝试使用不同的搜索关键词。"
        
        return base_message
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """
        获取错误统计信息
        用于系统监控和问题分析
        
        Returns:
            Dict[str, Any]: 错误统计信息
        """
        return {
            "error_count": self.error_count.copy(),
            "total_errors": sum(self.error_count.values()),
            "recent_errors": len(self.last_errors),
            "error_types": list(self.error_count.keys())
        }
    
    def clear_error_history(self):
        """
        清除错误历史记录
        用于重置错误统计和释放内存
        """
        self.error_count.clear()
        self.last_errors.clear()
        self.logger.info("错误历史记录已清除")

# 创建全局错误处理器实例
error_handler = ErrorHandler()

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_errors.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)