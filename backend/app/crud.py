from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from passlib.context import CryptContext
from pyorthanc import Orthanc
import logging

Orthanc = Orthanc('http://localhost:8042')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=pwd_context.hash(user.password), username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def add_news(db: AsyncSession, news: schemas.NewsAdd):
    db_news = models.News(title=news.title, content=news.content, image=news.image)
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

async def delete_news(db: AsyncSession, news_id: int):
    news = await db.execute(select(models.News).where(models.News.id == news_id))
    news = news.scalars().first()
    if news:
        await db.delete(news)
        await db.commit()
        return True
    return False

async def get_all_news(db: AsyncSession):
    result = await db.execute(select(models.News))
    return result.scalars().all()

async def get_news_by_id(db: AsyncSession, news_id: int):
    result = await db.execute(select(models.News).where(models.News.id == news_id))
    return result.scalars().first()

async def update_news(db: AsyncSession, news_id: int, news_data: schemas.NewsAdd):
    news = await get_news_by_id(db, news_id)
    if not news:
        return None
    # Update the fields
    news.title = news_data.title
    news.content = news_data.content
    news.image = news_data.image
    await db.commit()
    await db.refresh(news)
    return news

async def send_dicom_file_to_orthanc(dicom_file: bytes):
    try:
        # Отправляем DICOM файл на Orthanc
        response = await Orthanc.post_instances(dicom_file)  # Используем метод post_instances
        if response.get('success', False):  # Проверяем наличие ключа 'success' в ответе
            return {"message": "DICOM file successfully uploaded to Orthanc"}
        else:
            logging.error(f"Ошибка при отправке DICOM файла: {response.get('error', 'Unknown error')}")
            raise Exception(f"Ошибка при отправке: {response.get('error', 'Unknown error')}")
    except Exception as e:
        logging.error(f"Ошибка при отправке DICOM файла: {str(e)}")
        raise