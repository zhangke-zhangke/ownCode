



fastapi路由接参（平替flask的request请求上下文）
    路径参数
        Path()
    查询参数
        Query()
    请求体参数
        Body()
    表单
        Form()
    文件
        File()
    cookie
        Cookie()
    header
        Header()

    结合pydantic接参
        class ItemModel(BaseModel):
            name: str
            age: int

        # fastapi自动处理参数，a匹配路径参数；b匹配查询参数；c匹配请求体参数（fastapi会自动创建ItemModel的实例赋值到c）
        @app.post('/xxx')
        def fun(a: Annotated[str, Path(default=None)], b: str, c: ItemModel):
            print(a)
            print(b)
            print(c.name)
            print(c.age)

        # 注解（Annotated）a: Annotated[str, Path(default=None)] 理解为，标志a是一个str的路径参数
        # 同理，Annotated[pydanticModel, Path() | Query() | Body] 则使用pydantic数据模型方法附加到fastapi的参数元数据对象


fastapi路由拆分（蓝图）
    1、子文件引用ApiRouter创建子路由实例
        child = ApiRouter()
    2、主文件使用app.include_router(子路由实例, prefix='/xxx')集成子路由
        from fastapi import FastApi
        from .childrenRouter import child

        app = FastApi()
        app.include_router(child, prefix='/child')


