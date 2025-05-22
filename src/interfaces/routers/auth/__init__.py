from fastapi import APIRouter
 
router = APIRouter(
    prefix='/auth',
    tags=[
        'auth'
    ]
)

@router.post('/login')
async def login():
    return {}


@router.post('/refresh-token')
async def refresh():
    return {}