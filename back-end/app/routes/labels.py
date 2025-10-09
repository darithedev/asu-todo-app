from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.label import Label, LabelResponse, LabelCreate, LabelUpdate
from beanie import PydanticObjectId
from .auth import get_current_user, require_admin
from ..models.user import User

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("/", response_model=List[LabelResponse])
async def get_my_labels(current_user: User = Depends(get_current_user)):
    """Get labels for the current authenticated user"""
    try:
        labels = await Label.find(Label.user_id == current_user.id).to_list()
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
async def get_labels_by_user_admin(user_id: str, _: User = Depends(require_admin)):
    """Admin: Get all labels for a specific user"""
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
async def get_label(label_id: str, current_user: User = Depends(get_current_user)):
    """Get a specific label by ID if owned or admin"""
    try:
        label = await Label.get(PydanticObjectId(label_id))
        if not label:
            raise HTTPException(status_code=404, detail="Label not found")
        if label.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not authorized to view this label")
        return LabelResponse(
            id=str(label.id),
            name=label.name,
            color=label.color,
            description=label.description,
            user_id=str(label.user_id),
            created_at=label.created_at,
            updated_at=label.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid label ID: {str(e)}")

# Authenticated Endpoints
@router.post("/", response_model=LabelResponse)
async def create_label(
    label_data: LabelCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new label for the current user"""
    try:
        # Ensure unique label name per user
        existing = await Label.find_one(
            Label.user_id == current_user.id,
            Label.name == label_data.name
        )
        if existing:
            raise HTTPException(status_code=400, detail="Label name already exists for this user")

        label = Label(
            name=label_data.name,
            user_id=current_user.id,
            color=label_data.color,
            description=label_data.description
        )
        await label.insert()

        return LabelResponse(
            id=str(label.id),
            name=label.name,
            color=label.color,
            description=label.description,
            user_id=str(label.user_id),
            created_at=label.created_at,
            updated_at=label.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating label: {str(e)}")


@router.patch("/{label_id}", response_model=LabelResponse)
async def update_label(
    label_id: str,
    label_data: LabelUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update an existing label owned by the current user"""
    try:
        label = await Label.get(PydanticObjectId(label_id))
        if not label:
            raise HTTPException(status_code=404, detail="Label not found")
        if label.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this label")

        # If name changes, ensure uniqueness per user
        if label_data.name and label_data.name != label.name:
            conflict = await Label.find_one(
                Label.user_id == current_user.id,
                Label.name == label_data.name
            )
            if conflict:
                raise HTTPException(status_code=400, detail="Label name already exists for this user")

        if label_data.name is not None:
            label.name = label_data.name
        if label_data.color is not None:
            label.color = label_data.color
        if label_data.description is not None:
            label.description = label_data.description

        await label.save()

        return LabelResponse(
            id=str(label.id),
            name=label.name,
            color=label.color,
            description=label.description,
            user_id=str(label.user_id),
            created_at=label.created_at,
            updated_at=label.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating label: {str(e)}")


@router.delete("/{label_id}")
async def delete_label(
    label_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a label owned by the current user"""
    try:
        label = await Label.get(PydanticObjectId(label_id))
        if not label:
            raise HTTPException(status_code=404, detail="Label not found")
        if label.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this label")

        await label.delete()
        return {"message": "Label deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting label: {str(e)}")
