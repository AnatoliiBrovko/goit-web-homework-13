from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse], description='Over 10 requests/min', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_params(skip: int = 0, limit: int = Query(default=10),
                                first_name: Optional[str] = Query(default=None),
                                last_name: Optional[str] = Query(default=None),
                                email: Optional[str] = Query(default=None),
                                db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):

    contact = await repository_contacts.get_contacts(skip, limit, first_name, last_name, email, current_user, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact


@router.get("/birthdays", response_model=list[ContactResponse], description='Over 10 requests/min', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_birthdays(skip: int = 0, limit: int = Query(default=10), 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.get_contacts_birthdays(skip, limit, current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='Over 10 requests/min', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int, 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):

    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact


@router.post("/", response_model=ContactResponse, description='Over 3 requests/ 5 min', dependencies=[Depends(RateLimiter(times=3, minutes=5))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):

    new_contact = await repository_contacts.create_contact(body, current_user, db)
    return new_contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag(contact_id: int, 
                        db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):

    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact