from fastapi import APIRouter, HTTPException
from typing import List
from ..models.label import Label, LabelResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/", response_model=List[LabelResponse])
async def get_all_labels():
    """Get all labels"""
    labels = await Label.find_all().to_list()
    return labels

@router.get("/user/{user_id}", response_model=List[LabelResponse])
async def get_user_labels(user_id: str):
    """Get all labels for a specific user"""
    try:
        labels = await Label.find(Label.user_id == PydanticObjectId(user_id)).to_list()
        return labels
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID: {str(e)}")

@router.get("/{label_id}", response_model=LabelResponse)
async def get_label(label_id: str):
    """Get a specific label by ID"""
    try:
        label = await Label.get(PydanticObjectId(label_id))
        if not label:
            raise HTTPException(status_code=404, detail="Label not found")
        return label
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid label ID: {str(e)}")
