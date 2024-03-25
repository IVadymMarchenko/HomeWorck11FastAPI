from sqlalchemy import select, cast, Date, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.contacts.models import Contact
from src.schemas.checkschemas import CreateContactSchema, CreateContact
from datetime import datetime, timedelta
from sqlalchemy import func


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    smt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(smt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    smt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(smt)
    return contact.scalar_one_or_none()


async def create_contact(body: CreateContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: CreateContactSchema, db: AsyncSession):
    smt = select(Contact).filter_by(id=contact_id)
    contacts = await db.execute(smt)
    contact = contacts.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    smt = select(Contact).filter_by(id=contact_id)
    contacts = await db.execute(smt)
    contact = contacts.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_all_birthdays(db: AsyncSession):

    birthdays = await db.execute(select(Contact.birthday))
    return birthdays.scalars().all()


async def look_for_contact(db:AsyncSession,name_contact:str):
    query = select(Contact).filter(or_(Contact.name == name_contact,
                                       Contact.surname == name_contact,
                                       Contact.email == name_contact))
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    return contact



