from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, WebSocket, WebSocketDisconnect, APIRouter
from httpx import stream
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel
from backend.app import crud, schemas, auth
from backend.app.database import AsyncSessionLocal
from typing import Optional
import traceback
import base64
from pyorthanc import Orthanc
import aiofiles
import httpx
import asyncio
from starlette.responses import StreamingResponse
import random
import smtplib
from email.mime.text import MIMEText

OrthancAPI = Orthanc('http://orthanc:8042')

orthanc_url = "http://orthanc:8042"

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

class VerificationData(BaseModel):
    email: str
    code: str

app = FastAPI(root_path="/api")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:80",
    "http://frontend:80",
    "http://localhost:8042",
    "http://localhost:25",
    "http://localhost:1025",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(email: str, code: str):
    try:
        msg = MIMEText(f"Ваш код подтверждения: {code}")
        msg['Subject'] = 'Код подтверждения'
        msg['From'] = 'brykovbrykov17@gmail.com'
        msg['To'] = email

        with smtplib.SMTP('smtp', 25) as server:
            server.send_message(msg)
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/register/", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)


verification_codes = {}
@app.post("/token/")
async def login_for_access_token(login_data: LoginData, db: AsyncSession = Depends(get_db)):
    try:
        logging.debug(f"Login attempt for user {login_data.email}")
        user = await crud.get_user_by_email(db, email=login_data.email)
        if not user:
            logging.error("No user found with provided email.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        if not await crud.verify_password(login_data.password, user.hashed_password):
            logging.error("Password verification failed.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        code = generate_verification_code()
        verification_codes[login_data.email] = code
        logging.debug(f"Generated verification code for {login_data.email}: {code}")

        send_verification_email(login_data.email, code)
        logging.info(f"Verification code sent to {login_data.email}")

        return {"message": "Verification code sent to your email"}
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        logging.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/verify-code/")
async def verify_code(data: VerificationData):
    email = data.email
    code = data.code
    stored_code = verification_codes.get(email)
    if not stored_code or stored_code != code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification code")

    access_token = auth.create_access_token(data={"sub": email})
    del verification_codes[email]
    response = JSONResponse(content={"access_token": access_token, "message": "Successfully logged in"})
    response.set_cookie(key="authToken", value=access_token, httponly=True,
                        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return response


@app.post("/news/add/", response_model=schemas.News)
async def add_news(title: str = Form(...),
       content: str = Form(...),
       image: Optional[UploadFile] = File(None),
       db: AsyncSession = Depends(get_db)
    ):
    logging.debug(f"Title: {title}, Content: {content}, Image: {image.filename}")
    if not title or not content:
        raise HTTPException(status_code=400, detail="Необходимо указать заголовок и текст новости")
    try:
        image_base64 = None
        if image:
            image_data = await image.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

        news_data = schemas.NewsAdd(title=title, content=content, image=image_base64)
        db_news = await crud.add_news(db, news_data)
        return db_news
    except Exception as e:
        print("Ошибка при добавлении новости:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
@app.get("/news/", response_model=list[schemas.News])
async def get_news(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_news(db)

@app.delete("/news/{news_id}/", status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
   news_deleted = await crud.delete_news(db, news_id)
   if not news_deleted:
       raise HTTPException(status_code=404, detail="News not found")
   return {"message": "News successfully deleted"}

@app.get("/news/{news_id}/", response_model=schemas.News)
async def get_news_by_id(news_id: int, db: AsyncSession = Depends(get_db)):
    news_item = await crud.get_news_by_id(db, news_id)
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")
    return news_item

@app.put("/news/{news_id}/", response_model=schemas.News)
async def update_news(
    news_id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    existing_news = await crud.get_news_by_id(db, news_id)
    if not existing_news:
        raise HTTPException(status_code=404, detail="News not found")

    image_base64 = existing_news.image
    if image:
        image_data = await image.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

    updated_news_data = schemas.NewsAdd(
        title=title or existing_news.title,
        content=content or existing_news.content,
        image=image_base64
    )

    updated_news = await crud.update_news(db, news_id, updated_news_data)
    return updated_news


@app.post("/upload-dicom/")
async def upload_dicom(file: UploadFile = File(...)):
    try:
        # Сохраните файл временно
        temp_file_path = f"/tmp/{file.filename}"
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Загрузите файл в Orthanc
        with open(temp_file_path, 'rb') as dicom_file:
            dicom_data = dicom_file.read()
            response = OrthancAPI.post_instances(dicom_data)

        return {"message": "DICOM file uploaded successfully", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading DICOM file: {str(e)}")

@app.get("/studies/", response_model=list[schemas.Study])
async def get_studies():
    try:
        studies_response = OrthancAPI.get_studies()
        studies = []

        async with httpx.AsyncClient() as client:
            for study_id in studies_response:
                study_details = await fetch_study_details(client, study_id)  # Передаем клиент здесь
                study_info = {
                    "ID": study_details.get("ID"),
                    "LastUpdate": study_details.get("LastUpdate"),
                    "MedicalCardNumber": study_details.get("MainDicomTags", {}).get("MedicalCardNumber"),
                    "StudyInstanceUID": study_details.get("MainDicomTags", {}).get("StudyInstanceUID"),
                    "PatientBirthDate": study_details.get("PatientMainDicomTags", {}).get("PatientBirthDate"),
                    "PatientName": study_details.get("PatientMainDicomTags", {}).get("PatientName"),
                }
                studies.append(study_info)

        return studies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching studies: {str(e)}")

async def fetch_study_details(client, study_id):
    orthanc_server_url = "http://orthanc:8042"  # замените на фактический адрес Orthanc
    response = await client.get(f"{orthanc_server_url}/studies/{study_id}")
    response.raise_for_status()
    return response.json()


@app.delete("/studies/{study_id}/", status_code=status.HTTP_204_NO_CONTENT, response_class=JSONResponse)
async def delete_study(study_id: str):
    try:
        OrthancAPI.delete_studies_id(study_id)
        return {"message": "Study successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Study not found: {str(e)}")


@app.get("/studies/{study_id}/series", response_model=list[schemas.Series])
async def get_series_for_study(study_id: str):
    try:
        async with httpx.AsyncClient() as client:

            study_details = await fetch_study_details(client, study_id)

            series_ids = study_details.get("Series", [])

            series_info_list = await fetch_series_details(client, series_ids)

        return series_info_list

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code,
                            detail=f"Error retrieving series: {exc.response.text}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")


async def fetch_series_details(client, series_ids):
    series_info_list = []
    for series_id in series_ids:
        # Fetch series details
        series_info = await fetch_series_info(client, series_id)

        # Add formatted series info to the list
        series_info_list.append({
            "series_id": series_id,
            "instance_number": series_info.get("MainDicomTags", {}).get("SeriesNumber"),
            "series_description": series_info.get("MainDicomTags", {}).get("SeriesDescription"),
            "number_of_instances": series_info.get("NumberOfInstances"),
        })
    return series_info_list


async def fetch_series_info(client, series_id):
    orthanc_server_url = "http://orthanc:8042"
    response_series = await client.get(f"{orthanc_server_url}/series/{series_id}")
    response_series.raise_for_status()
    return response_series.json()


@app.get("/series/{series_id}/instances", response_model=list[str])
async def get_instances_for_series(series_id: str):
    try:
        async with httpx.AsyncClient() as client:
            series_info = await fetch_series_info(client, series_id)

        instances = series_info.get("Instances", [])
        return instances

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code,
                            detail=f"Error retrieving instances: {exc.response.text}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")


@app.get("/instances/{instance_id}/tags", response_model=dict)
async def get_dicom_tags_for_instance(instance_id: str):
    try:
        async with httpx.AsyncClient() as client:
            instance_info = await fetch_instance_info(client, instance_id)

        all_tags = instance_info.get("DicomTags", instance_info)
        return all_tags

    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")


async def fetch_instance_info(client: httpx.AsyncClient, instance_id: str) -> dict:
    orthanc_server_url = "http://orthanc:8042"
    try:
        response_instance = await client.get(f"{orthanc_server_url}/instances/{instance_id}/simplified-tags")
        response_instance.raise_for_status()
        return response_instance.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error retrieving DICOM tags: {exc.response.text}")


@app.websocket("/ws/archive-status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            study_id = await websocket.receive_text()
            job_id = await start_dicom_archive_creation(study_id)
            await monitor_job_status(websocket, study_id, job_id)
    except WebSocketDisconnect:
        pass

async def start_dicom_archive_creation(study_id: str) -> str:
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{orthanc_url}/studies/{study_id}/archive",
            json={"Asynchronous": True}
        )
        response.raise_for_status()
        job_info = response.json()
        return job_info["ID"]

async def monitor_job_status(websocket: WebSocket, study_id: str, job_id: str):
    async with httpx.AsyncClient(timeout=None) as client:
        job_url = f"{orthanc_url}/jobs/{job_id}"
        while True:
            response = await client.get(job_url)
            response.raise_for_status()
            job_status = response.json()

            await websocket.send_json({
                "Progress": job_status.get("Progress", 0),
                "State": job_status.get("State", "Unknown")
            })

            if job_status["Progress"] == 100 and job_status["State"] == "Success":
                await websocket.send_text(f"Job completed: {job_id}")
                break

            await asyncio.sleep(2)

@app.get("/download/{study_id}")
def download_dicom_archive(study_id: str):
    with httpx.Client(timeout=None) as client:
        response = client.get(f"{orthanc_url}/studies/{study_id}/archive")
        response.raise_for_status()

        if response.is_error:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return StreamingResponse(content=response.iter_bytes(), media_type='application/zip', headers={'Content-Disposition': f'attachment; filename="{study_id}.zip"'})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)