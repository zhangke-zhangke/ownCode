from typing import Optional, TypeVar


# 表示泛型
T = TypeVar('T')


class CustomerException(Exception):
    def __init__(self, msg: str, raise_data: dict=None):
        super().__init__(msg)
        self.raise_data = raise_data

    def __str__(self):
        return self.args[0]

    # def get_raise_key_data(self, key: str) -> Optional[object | None]:
    def get_raise_key_data(self, key: str) -> T:
        return self.raise_data.get(key, None)


if __name__ == '__main__':

    try:
        raise CustomerException('自定义异常', {'key': 'value'})
    except Exception as e:
        print(e.get_raise_key_data('key'))



