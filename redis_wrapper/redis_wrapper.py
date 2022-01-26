import json
import redis as rds
from functools import wraps
from inspect import signature

class RedisCacheWrapper:
    _base_key = "memory:cache"

    def __init__(self, redis_host, redis_port):
        self.rds = rds.Redis(redis_host, redis_port, decode_responses=True)
    
    def __call__(self, ex=10):
        """
        prefix: key前缀
        ex: time to live(s)
        """
        def wrapper(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                _key = self._generate_key(func, args, kwargs)
                value = self._get(_key)
                if value is None:
                    value = func(*args, **kwargs)
                    # 如果返回的数据为None，直接返回不保存。
                    if value:
                        self._save(_key, value, ex=ex)
                return value
            return _wrapper
        return wrapper

    @classmethod
    def _generate_key(cls, func, args, kwargs):
        """
        - args中存在None如何处理
        """
        sig = signature(func)

        parameter_list = list(sig.parameters.keys())
        emp_args_list = [kwargs[item] for item in parameter_list if item in kwargs]

        if parameter_list[0] in ("self", "cls"):
            args = args[1:]

        # 获取所有的输入参数
        all_input = list(args) + emp_args_list
        # 检测所有的输入参数，必须为str/int/float/None。最后统一转换为str类型
        all_input_stred = []
        for item in all_input:
            if not isinstance(item, (str, int, float, type(None))):
                raise ValueError("input paramenter must in (str, int, float).")
            all_input_stred.append(str(item))

        sub_key_parameter = ":".join(all_input_stred)
        sub_key_function_name = f"{func.__module__}.{func.__name__}"

        return f"{cls._base_key}:{sub_key_function_name}:{sub_key_parameter}"

    def _save(self, key, value, ex=None):
        if isinstance(value, dict):
            self.rds.set(key, json.dumps(value), ex=ex)
        else:
            raise ValueError(f"value must be dict, but input is{type(value)}")

    def _get(self, key):
        value = self.rds.get(key)
        value = json.loads(value) if value else None
        return value