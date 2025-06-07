import json
import io
import base64
import asyncio
import os

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Response

from app.database import User
from app.schemas import ImagePrompt
from app.users import current_active_user


router = APIRouter(tags=["image"])


@router.post("/generate", response_class=Response)
async def generate_image(
    imagePrompt: ImagePrompt,
    user: User = Depends(current_active_user),
):
    # Call the external API
    url = os.getenv("IMAGE_GEN_API_URL")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('IMAGE_GEN_API_KEY')}",
    }
    data = {
        "model": "gpt-image-1",
        "prompt": imagePrompt.imagePrompt,
        "n": 1,
        "size": "1024x1024"
    }
    print("url", url)
    print("headers", headers)
    print("data", data)
    image_data = {}
    
    # image_data = {
    #     "created": 1749327175,
    #     "background": "opaque",
    #     "data": [],
    #     "output_format": "png",
    #     "quality": "high",
    #     "size": "1024x1024",
    #     "usage": {
    #         "input_tokens": 36,
    #         "input_tokens_details": {
    #             "image_tokens": 0,
    #             "text_tokens": 36
    #         },
    #         "output_tokens": 4160,
    #         "total_tokens": 4196
    #     }
    # }
    # await asyncio.sleep(1)
    # image_b64str = image_data["data"][0]["b64_json"]
    # return image_b64str


    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Image gen API returned status {response.status}"
                    )
                image_data = await response.json()
                image_b64str = image_data["data"][0]["b64_json"]
                return image_b64str
        except aiohttp.ClientError as e:
            print(f"Error calling image gen service: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error calling image gen service: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing image gen data: {str(e)}"
            )
