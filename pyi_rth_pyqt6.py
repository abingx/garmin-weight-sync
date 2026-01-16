"""
PyInstaller Runtime Hook
修复打包后 inspect.getsource() 失败的问题
"""
import sys
import os

# 禁用 logfire 的 pydantic 集成（会导致 inspect.getsource 错误）
os.environ['LOGFIRE_SKIP_PYDANTIC_PLUGIN'] = '1'
os.environ['PYDANTIC_DISABLE_PYDANTIC_V2_PLUGINS'] = '1'

# 修改 inspect 模块，使其在找不到源码时返回空字符串而不是抛出异常
import inspect

_original_getsource = inspect.getsource

def _patched_getsource(object):
    """修补后的 getsource，在打包环境中返回空字符串"""
    try:
        return _original_getsource(object)
    except (OSError, TypeError):
        # 返回一个占位符字符串
        return "# Source code not available in frozen application"

inspect.getsource = _patched_getsource

# 同样修补 getsourcelines
_original_getsourcelines = inspect.getsourcelines

def _patched_getsourcelines(object):
    """修补后的 getsourcelines"""
    try:
        return _original_getsourcelines(object)
    except (OSError, TypeError):
        # 返回一个占位符
        return ["# Source code not available in frozen application"], 1

inspect.getsourcelines = _patched_getsourcelines

# 同样修补 getsourcefile
_original_getsourcefile = inspect.getsourcefile

def _patched_getsourcefile(object):
    """修补后的 getsourcefile"""
    try:
        return _original_getsourcefile(object)
    except (OSError, TypeError):
        return None

inspect.getsourcefile = _patched_getsourcefile
