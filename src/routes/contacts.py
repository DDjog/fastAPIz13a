from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactNotes, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from typing import List

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse],
                 description='No more than 10 requests per minute',
                 dependencies=[Depends(RateLimiter(times=10, seconds=60))]
            )
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):

    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    return contact


@router.get("/birthday_ahead/{days}", response_model=List[ContactResponse])
async def read_contacts_birthday_ahead(days: int, db: Session = Depends(get_db),
                                       current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_birthday_ahead( days, current_user, db )

    return contacts


@router.get("/firstname/{first_name}", response_model=List[ContactResponse])
async def read_firstname_contacts(first_name: str, db: Session = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_by_firstname(first_name, current_user, db)
    
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact or contacts not found")
    
    return contacts


@router.get("/secondname/{second_name}", response_model=List[ContactResponse])
async def read_secondname_contacts(second_name: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_by_secondname(second_name, current_user, db)
    
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact or contacts not found")
    
    return contacts


@router.get("/firstandsecondname/{first_name}/{second_name}", response_model=List[ContactResponse])
async def read_firstsecondname_contacts(first_name: str, second_name: str, db: Session = Depends(get_db),
                                        current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_by_first_and_second_name(first_name, second_name, 
                                                                               current_user, db)
    
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact or contacts not found")
    
    return contacts


@router.get("/email/{contact_email}", response_model=List[ContactResponse])
async def read_email_contacts(contact_email: str, db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_by_email(contact_email, current_user, db)
    
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact or contacts not found")
    
    return contacts


@router.get("/note/{contact_id}", response_model=str)
async def read_note_contact(contact_id: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):

    contact = await repository_contacts.get_contact_notes(contact_id, current_user, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    if contact.notes is None:
        return ""
    
    return contact.notes


@router.post("/", response_model=ContactBase,
                 description='No more than 2 contact creations per minute',
                 dependencies=[Depends(RateLimiter(times=2, seconds=60))]
            )
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactBase)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    return contact


@router.put("/note/{contact_id}", response_model=ContactNotes)
async def update_contact_notes(notes: str, contact_id: int, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    
    contact = await repository_contacts.update_contact_notes(contact_id, notes, current_user, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    return contact


@router.delete("/{contact_id}", response_model=ContactBase)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    return contact


