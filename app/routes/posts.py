import json
import os

import aiohttp
from fastapi import APIRouter, Depends, HTTPException

from app.database import User
from app.schemas import PostCreate, PostResponse
from app.users import current_active_user

router = APIRouter(tags=["posts"])


@router.post("/", response_model=list[PostResponse])
async def create_post(
    post: PostCreate,
    user: User = Depends(current_active_user),
):
    # Call the external API
    url = os.getenv("PREDICTION_API_URL")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PREDICTION_API_KEY')}",
    }
    data = {
        "form": {
            "brandName": post.brandName,
            "location": post.location,
            "industry": post.industry,
            "websiteURL": post.websiteURL
        }
    }

    # posts_data = [
    #     {
    #         "id": "1",
    #         "caption": "Building a greener future with Magna Steel's sustainable TMT bars. Quality, strength, and environmental responsibility in every piece. 🌿 #SustainableSteel #BuildWithMagna",
    #         "image_prompt": "A construction site at dawn showcasing a stack of gleaming TMT bars with a backdrop of lush greenery, emphasizing the fusion of modern infrastructure and nature."
    #     },
    #     {
    #         "id": "2",
    #         "caption": "Building a sustainable future with Magna TMT bars. Unmatched quality and environmental responsibility. #SteelRevolution #SustainableStrength",
    #         "image_prompt": "A vibrant construction site with workers using sturdy TMT bars, surrounded by lush green landscapes. Highlight the TMT bars and include elements representing sustainability, such as wind turbines or solar panels."
    #     },
    #     {
    #         "id": "3",
    #         "caption": "Building a sustainable future with Magna Steel TMT bars! 🌍 #GreenerStrongerBetter",
    #         "image_prompt": "A dynamic image of TMT bars in a construction site, with a backdrop of lush green landscapes symbolizing sustainability. Include elements that convey strength and eco-friendliness, such as clear skies and thriving plants."
    #     }
    # ]
    # response_data = []
    # for i, post in enumerate(posts_data):
    #     post["id"] = f"{i + 1}"
    #     response_data.append(PostResponse(**post))
    # return response_data
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Prediction API returned status {response.status}"
                    )
                prediction_data = await response.json()
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling prediction service: {str(e)}"
            )

    # Save the post to database
    # db_post = Post(**post.model_dump(), user_id=user.id, prediction_data=prediction_data)
    # db.add(db_post)
    # await db.commit()
    # await db.refresh(db_post)
    # return db_post
    try:
        posts_data = json.loads(prediction_data["text"].replace('```json','').replace('```',''))
        response_data = []
        for i, post in enumerate(posts_data):
            post["id"] = f"{i + 1}"
            response_data.append(PostResponse(**post))
        return response_data
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Error parsing prediction data"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing prediction data: {str(e)}"
        )
