from pydantic import BaseModel

class AssetTagBase(BaseModel):
    id_asset: int
    id_tag: int

class AssetTagCreate(AssetTagBase):
    pass

class AssetTagResponse(AssetTagBase):
    class Config:
        from_attributes = True
