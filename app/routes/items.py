from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class Item(ItemCreate):
    id: int


_store: dict[int, Item] = {}
_next_id: int = 1


def _reset_store() -> None:
    global _next_id
    _store.clear()
    _next_id = 1


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _store[item.id] = item
    _next_id += 1
    return item


@router.get("", response_model=list[Item])
def list_items() -> list[Item]:
    return list(_store.values())


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = _store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemCreate) -> Item:
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, **payload.model_dump())
    _store[item_id] = updated
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if _store.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item not found")
