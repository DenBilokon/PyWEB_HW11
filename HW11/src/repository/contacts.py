from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel
from datetime import date


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_contact_by_phone(phone_number: str, db: Session):
    contact = db.query(Contact).filter_by(phone_number=phone_number).first()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.other_data = body.other_data
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(keyword: str, db: Session):
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{keyword}%")) |
        (Contact.last_name.ilike(f"%{keyword}%")) |
        (Contact.email.ilike(f"%{keyword}%"))
    ).all()
    return contacts


async def upcoming_birthdays(days: int, db: Session):
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).all()
    for contact in contacts:
        td = contact.birthday.replace(year=current_year) - today
        if 0 <= td.days <= days:
            contacts_with_birthdays.append(contact)
        else:
            continue
    print(contacts_with_birthdays)
    return contacts_with_birthdays
