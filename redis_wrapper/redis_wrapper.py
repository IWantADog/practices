import json
import redis as rds
from functools import wraps
from inspect import signature, Parameter

class RedisCacheWrapper:
    _base_key = "memory:cache"

    def __init__(self, redis_host, redis_port):
        self.rds = rds.Redis(redis_host, redis_port, decode_responses=True)
    
    def __call__(self, prefix, ex=10):
        """
        prefix: key前缀
        ex: time to live(s)
        """
        def wrapper(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                _key = self._generate_key(prefix, func, args, kwargs)
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
    def _generate_key(cls, prefix, func, args, kwargs):
        """
        根据function的形参，生成redis key
        - args中存在None如何处理
            - 直接转化为字符串`str(None)`
        - 如何处理function中存在default的情况
        """
        sig = signature(func)
        paramenter = sig.parameters
        parameter_list = list(paramenter.keys())

        if parameter_list[0] in ("self", "cls"):
            args = args[1:]
            parameter_list = parameter_list[1:]

        emp_args_list = []
        for item in parameter_list[len(args):]:
            if item in kwargs:
                emp_args_list.append(kwargs[item])
            else:
                # 对于未传入的参数，使用默认值
                _default = paramenter[item].default
                if _default == Parameter.empty:
                    raise ValueError(f"{func.__name__} paramenter {item} did not defind default")
                emp_args_list.append(_default)

        # 获取所有的输入参数
        all_input = list(args) + emp_args_list
        # 检测所有的输入参数，必须为str/int/float/None。最后统一转换为str类型
        all_input_stred = []
        for item in all_input:
            if not isinstance(item, (str, int, float, type(None))):
                raise ValueError("input paramenter must in (str, int, float, None).")
            all_input_stred.append(str(item))

        if len(parameter_list) != len(all_input_stred):
            raise ValueError("generate key error!")

        sub_key_parameter = ":".join(all_input_stred)
        return f"{cls._base_key}:{prefix}:{sub_key_parameter}"

    def _save(self, key, value, ex=None):
        if isinstance(value, dict):
            self.rds.set(key, json.dumps(value), ex=ex)
        else:
            raise ValueError(f"value must be dict, but input is{type(value)}")

    def _get(self, key):
        value = self.rds.get(key)
        value = json.loads(value) if value else None
        return value