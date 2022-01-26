import json
from redis import Redis
from unittest import TestCase, main
from redis_wrapper.redis_wrapper import RedisCacheWrapper

host = '127.0.0.1'
port = 6379
memory_cache = RedisCacheWrapper(host, port)

class CachedClass:
    def func_in_class(self, version, a=1, b=2):
        return {
            "version": version,
            "a": a,
            "b": b,
        }
    
    cached_func_in_class = memory_cache(prefix="test", ex=100)(func_in_class)

def func(a, b=2, c=1):
    return {
        "a": a,
        "b": b,
        "c": c,
    }

cached_func = memory_cache(prefix="test-2", ex=100)(func)

class TestCaseForRedisCacheWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rds = Redis(host, port)
        cls.need_clear_keys = None
    
    def tearDown(self):
        if self.need_clear_keys is not None:
            self.rds.delete(*self.need_clear_keys)
        
    def test_wrapper_static_function(self):
        real_return = cached_func(1,2,3)
        cached_return = cached_func(1,2,3)

        self.assertEqual(real_return, cached_return)
        _key = RedisCacheWrapper._generate_key(
            "test-2",
            func,
            args=[1,2,3],
            kwargs={}
        )
        print(_key)
        self.need_clear_keys = [_key]

        str_value = self.rds.get(_key)
        value_from_redis = json.loads(str_value)
        self.assertEqual(value_from_redis, real_return)
    
    def test_wrapper_static_function_with_kwargs(self):
        """测试function参数包含kwargs的情况"""
        real_return = cached_func(1,2,c=4)
        cached_return = cached_func(1,2,c=4)

        self.assertEqual(real_return, cached_return)
        _key = RedisCacheWrapper._generate_key(
            "test-2",
            func,
            args=[1,2],
            kwargs={"c": 4}
        )

        print(_key)
        self.need_clear_keys = [_key]
        str_value = self.rds.get(_key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(value_from_redis, real_return)

    def test_wrapper_static_function_with_None(self):
        """测试function参数包含None的情况"""
        real_return = cached_func(1,None,c=4)
        cached_return = cached_func(1,None,c=4)

        self.assertEqual(real_return, cached_return)
        _key = RedisCacheWrapper._generate_key(
            "test-2",
            func,
            args=[1,None],
            kwargs={"c": 4}
        )
        print(_key)
        self.need_clear_keys = [_key]
        str_value = self.rds.get(_key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(value_from_redis, real_return)
    
    def test_wrapper_static_function_with_default_value(self):
        """测试funcion参数中包含默认值的情况"""
        real_return = func(1, c=3)
        cached_return = cached_func(1, c=3)
        self.assertEqual(real_return, cached_return)
        _key = RedisCacheWrapper._generate_key(
            "test-2", func, args=[1], kwargs={"c": 3}
        )

        self.assertEqual(_key, 'memory:cache:test-2:1:2:3')

        self.need_clear_keys = [_key]
        str_value = self.rds.get(_key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(real_return, value_from_redis)

    def test_wrapper_class_function(self):
        """测试装饰class.functions"""
        a = CachedClass()
        real_return = a.func_in_class('version_code', 2, 3)
        cached_return = a.cached_func_in_class('version_code', 2, 3)
        self.assertEqual(real_return, cached_return)

        key = RedisCacheWrapper._generate_key(
            "test",
            a.func_in_class,
            args=['version_code', 2, 3],
            kwargs={}
        )
        self.need_clear_keys = [key]

        str_value = self.rds.get(key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(real_return, value_from_redis)
    
    def test_wrapper_class_function_with_None(self):
        """测试输入参数中包含None的情况"""
        a = CachedClass()
        real_return = a.func_in_class("version_code", None, 3)
        cached_return = a.cached_func_in_class("version_code", None, 3)
        self.assertEqual(real_return, cached_return)

        key = RedisCacheWrapper._generate_key(
            "test",
            a.func_in_class,
            args=['version_code', None, 3],
            kwargs={}
        )
        self.need_clear_keys = [key]

        str_value = self.rds.get(key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(real_return, value_from_redis)
    
    def test_wrapper_class_function_with_kwargs(self):
        """测试输入的参数使用kwargs的情况"""
        a = CachedClass()
        real_return = a.func_in_class(version="version_code", b=3, a=None)
        cache_return = a.cached_func_in_class(version="version_code", b=3, a=None)
        self.assertEqual(real_return, cache_return)

        key = RedisCacheWrapper._generate_key(
            "test",
            a.func_in_class, 
            args=[],
            kwargs={"version": "version_code", "b": 3, "a":None}
        )
        print(key)
        
        str_value = self.rds.get(key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(real_return, value_from_redis)

    def test_wrappser_class_function_with_default(self):
        a = CachedClass()
        real_return = a.func_in_class("version", b=3)
        cache_return = a.cached_func_in_class("version", b=3)
        self.assertEqual(real_return, cache_return)

        key = RedisCacheWrapper._generate_key(
            "test",
            a.func_in_class,
            args=['version'],
            kwargs={"b": 3}
        )
        self.assertEqual(key, "memory:cache:test:version:1:3")

        str_value = self.rds.get(key)
        print(f"get from redis {str_value}")
        value_from_redis = json.loads(str_value)
        self.assertEqual(real_return, value_from_redis)


if __name__ == '__main__':
    main()
