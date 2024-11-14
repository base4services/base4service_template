from . import router


@router.get('/healthy')
async def healthy():
    return {'healthy': True}
