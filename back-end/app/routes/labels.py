from fastapi import APIRouter, HTTPException
from typing import List
from ..models.label import Label, LabelResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/", response_model=List[LabelResponse])
async def get_all_labels():
    """Get all labels"""
    try:
        labels = await Label.find_all().to_list()
        # Convert to response format manually
        return [LabelResponse(
            id=str(label.id),
            name=label.name,
            color=label.color,
            description=label.description,
            user_id=str(label.user_id),
            created_at=label.created_at,
            updated_at=label.updated_at
        ) for label in labels]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/user/{user_id}", response_model=List[LabelResponse])
async def get_user_labels(user_id: str):
    """Get all labels for a specific user"""
    try:
        labels = await Label.find(Label.user_id == PydanticObjectId(user_id)).to_list()
        return [LabelResponse(
            id=str(label.id),
            name=label.name,
            color=label.color,
            description=label.description,
            user_id=str(label.user_id),
            created_at=label.created_at,
            updated_at=label.updated_at
        ) for label in labels]
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
