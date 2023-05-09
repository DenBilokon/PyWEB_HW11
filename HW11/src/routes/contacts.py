from typing import List
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse

from fastapi import APIRouter, Depends, HTTPException, Path, status
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found!')
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact_email = await repository_contacts.get_contact_by_email(body.email, db)
    contact_phone_number = await repository_contacts.get_contact_by_phone(body.phone_number, db)
    if contact_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists')
    if contact_phone_number:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Phone number is exists')
    contact = await repository_contacts.create(body, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found!')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found!')
    return contact


@router.get('/search/keyword={keyword}', response_model=List[ContactResponse])
async def search(keyword: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contact(keyword, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Contacts with keyword: {keyword} not found!')
    return contacts


@router.get('/birthdays/{days}', response_model=List[ContactResponse])
async def upcoming_birthdays_list(days: int, db: Session = Depends(get_db)):
    birthdays = await repository_contacts.upcoming_birthdays(days, db)
    return birthdays
