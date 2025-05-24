from pydantic import BaseModel, ConfigDict

class ImageBase(BaseModel):
    file_name: str

class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int