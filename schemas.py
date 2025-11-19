"""
Database Schemas for Suhail Yemen Model Schools Website

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class News(BaseModel):
    title: str = Field(..., description="News title in Arabic")
    body: str = Field(..., description="Full news content in Arabic")
    image_url: Optional[str] = Field(None, description="Image URL for the news item")
    published: bool = Field(True, description="Whether the news item is published")

class GalleryImage(BaseModel):
    url: str = Field(..., description="Image URL")
    caption: Optional[str] = Field(None, description="Short caption in Arabic")
    album: Optional[str] = Field(None, description="Album or category name")

class AdmissionApplication(BaseModel):
    student_name: str = Field(..., description="Student full name")
    stage: str = Field(..., description="Requested stage: روضة، تمهيدي، أساسي، ثانوي")
    birthdate: Optional[str] = Field(None, description="Birthdate (YYYY-MM-DD)")
    guardian_name: str = Field(..., description="Guardian full name")
    phone: str = Field(..., description="Primary contact phone number")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    address: Optional[str] = Field(None, description="Home address")
    notes: Optional[str] = Field(None, description="Additional notes")

class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., description="Message body")

class ProgramStage(BaseModel):
    key: str = Field(..., description="Identifier: nursery, kg, basic, secondary")
    title: str = Field(..., description="Stage title in Arabic")
    description: str = Field(..., description="Short description in Arabic")
    features: Optional[List[str]] = Field(default_factory=list, description="Key features list")
