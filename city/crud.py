from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def get_single_city(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_city(db: AsyncSession, city: schemas.CityBase):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityBase):
    db_city = await get_single_city(db, city_id)
    for field, value in city.dict(exclude_unset=True).items():
        setattr(db_city, field, value)
    await db.commit()
    return db_city


async def delete_city(db: AsyncSession, city_id: int):
    city = await get_single_city(db, city_id)
    await db.delete(city)
    await db.commit()
