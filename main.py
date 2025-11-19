import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import db, create_document, get_documents
from schemas import News, GalleryImage, AdmissionApplication, ContactMessage, ProgramStage

app = FastAPI(title="Suhail Yemen Model Schools API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Suhail Yemen Schools Backend Ready"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()
            except Exception:
                pass
        else:
            response["database"] = "❌ Not Connected"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# ---------- Public Endpoints ----------

@app.get("/api/news", response_model=List[News])
def list_news(limit: int = 20):
    docs = get_documents("news", {}, limit)
    # Convert ObjectId to string-safe dicts
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/api/admissions")
def submit_application(app_data: AdmissionApplication):
    try:
        app_id = create_document("admissionapplication", app_data)
        return {"status": "ok", "id": app_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def submit_contact(msg: ContactMessage):
    try:
        msg_id = create_document("contactmessage", msg)
        return {"status": "ok", "id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/gallery", response_model=List[GalleryImage])
def list_gallery(limit: int = 50):
    docs = get_documents("galleryimage", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/stages", response_model=List[ProgramStage])
def list_stages():
    # Seed defaults if empty
    existing = get_documents("programstage", {}, 10)
    if not existing:
        defaults = [
            ProgramStage(key="nursery", title="الروضة", description="بيئة تربوية آمنة لتنمية مهارات الطفل.", features=["أنشطة تفاعلية", "رعاية متميزة", "فصول مهيأة"]),
            ProgramStage(key="kg", title="التمهيدي", description="تهيئة الطفل للمرحلة الأساسية بالمهارات الأساسية.", features=["تركيز على القراءة والكتابة", "تنمية شخصية الطفل"]),
            ProgramStage(key="basic", title="الأساسي", description="تعليم أساسي متكامل وفق أحدث المناهج.", features=["مختبرات وتجارب", "تعلم نشط"]),
            ProgramStage(key="secondary", title="الثانوي", description="تأهيل أكاديمي قوي للاستعداد للجامعة.", features=["معامل حاسوب", "مدرسون متخصصون"]),
        ]
        for item in defaults:
            try:
                create_document("programstage", item)
            except Exception:
                pass
        existing = get_documents("programstage", {}, 10)
    for d in existing:
        d.pop("_id", None)
    return existing

# Simple schema exposure for admin tools (optional)
class SchemaItem(BaseModel):
    name: str
    fields: List[str]

@app.get("/schema", response_model=List[SchemaItem])
def get_schema():
    return [
        SchemaItem(name="news", fields=list(News.model_fields.keys())),
        SchemaItem(name="galleryimage", fields=list(GalleryImage.model_fields.keys())),
        SchemaItem(name="admissionapplication", fields=list(AdmissionApplication.model_fields.keys())),
        SchemaItem(name="contactmessage", fields=list(ContactMessage.model_fields.keys())),
        SchemaItem(name="programstage", fields=list(ProgramStage.model_fields.keys())),
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
