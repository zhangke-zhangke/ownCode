from fastapi import APIRouter


child = APIRouter()

@child.get('/childRouter')
def children():
    return "tatata"
