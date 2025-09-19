from fastapi import FastAPI, Request, Query, Body, Path, HTTPException, Response
from pydantic import BaseModel, field_validator, Field
from typing import Annotated, Literal
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import traceback
from childRouter import child


app = FastAPI()
app.include_router(child, prefix='/child')

@app.exception_handler(Exception)
def exception_handler(r: Request, e: Exception):
    print('全局异常捕获')
    print(e)

    # 请求外层response响应
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({
            "code": 500,
            "msg": "操作失败",
            "data": "",
        }),
    )


class dataDantic(BaseModel):
    t: str = Field(title='这是t', description='login入参t')
    rp: str

    @classmethod
    @field_validator('rp')
    def validate_tttt(cls, v):
        if len(v) < 3:
            raise ValueError('t must be at least 3 characters long')
        return v


@app.get('/login')
# def login(rp: str =  Query('12345', max_length=10)):
# def login(rp: Annotated[dataDantic, Query()]):
def login(rp: str, t: str):
    print(rp)
    return 'this is login page'


class Item(BaseModel):
    name: str
    age: int
    readme: str | None = None

    model_config = {
        "json_schema_extra": {
            'name': '张科',
            'age': 23,
            'readme': None,
        }
    }

@app.post('/testPost')
# def testPost(t: Annotated[str | None, Query()], item: Annotated[Item, Body()]):
# def testPost(item: Annotated[Item, Body(embed=True)], t: str | None):
def testPost(t: str | None, item: Item):
    '''
    测试post请求
    :param t:
    :param item:
    :return:
    '''
    print(item.name)
    print(item.age)
    print(item.readme)
    return 'this is testPost page'


class err(BaseModel):
    isError: bool

@app.post('/defineResponse')
def defineResponse(isError: Annotated[err, Query()]):
    if isError:
        raise Exception('this is defineResponse page')
    return {'code': 200, 'msg': 'success', 'data':[]}




if __name__ == '__main__':
    uvicorn.run(app)

    # it = Item(name='zhangke', age=23)
    # print(it)






