from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from app.storage.models import AddressPhoneData
from app.api.deps.repository_dependency import provide_storage_service
from app.services.storage_service import StorageService
from app.exceptions.repository_exceptions import (
    PhoneNotFoundException,
    InsertionFailedException,
    UpdateFailedException,
    DeletionFailedException,
    AddressAlreadyExistsException,
)
from app.api.schemas.responses import AddressResponse

router = APIRouter()


@router.get(
    "/get/{phone}",
    response_model=AddressResponse,
    summary="Получить адрес по номеру телефона",
    description="Возвращает адрес по номеру телефона из хранилища Redis",
    responses={
        404: {
            "description": "Номер телефона не найден",
            "content": {
                "application/json": {"example": {"detail": "Номер телефона не найден"}}
            },
        }
    },
)
async def get_address(
    service: Annotated[StorageService, Depends(provide_storage_service)],
    phone: str = Path(description="Номер телефона"),
):
    try:
        address = service.get_address_by_phone(phone)
        return AddressResponse(address=address)
    except PhoneNotFoundException:
        raise HTTPException(status_code=404, detail="Номер телефона не найден")


@router.put(
    "/insert",
    summary="Вставить связку адрес-телефон",
    description="Вставляет связку адрес-телефон в хранилище Redis",
    responses={
        409: {
            "description": "Номер телефона уже существует",
            "content": {
                "application/json": {
                    "example": {"detail": "Номер телефона уже существует"}
                }
            },
        },
        500: {
            "description": "Вставка данных не удалась",
            "content": {
                "application/json": {"example": {"detail": "Вставка данных не удалась"}}
            },
        },
    },
)
async def insert_address_phone(
    data: AddressPhoneData,
    service: Annotated[StorageService, Depends(provide_storage_service)],
):
    try:
        service.insert_phone_address_info(data)
        return {"detail": "Вставка успешна"}
    except AddressAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Номер телефона уже существует")
    except InsertionFailedException:
        raise HTTPException(status_code=500, detail="Вставка данных не удалась")


@router.post(
    "/update",
    summary="Обновить связку адрес-телефон",
    description="Обновляет связку адрес-телефон в хранилище Redis",
    responses={
        404: {
            "description": "Номер телефона не найден",
            "content": {
                "application/json": {"example": {"detail": "Номер телефона не найден"}}
            },
        },
        500: {
            "description": "Обновление данных не удалось",
            "content": {
                "application/json": {
                    "example": {"detail": "Обновление данных не удалось"}
                }
            },
        },
    },
)
async def update_address_phone(
    data: AddressPhoneData,
    service: Annotated[StorageService, Depends(provide_storage_service)],
):
    try:
        service.update_phone_address_info(data)
        return {"detail": "Обновление успешно"}
    except PhoneNotFoundException:
        raise HTTPException(status_code=404, detail="Номер телефона не найден")
    except UpdateFailedException:
        raise HTTPException(status_code=500, detail="Обновление данных не удалось")


@router.delete(
    "/delete/{phone}",
    summary="Удалить связку адрес-телефон",
    description="Удаляет связку адрес-телефон из хранилища Redis по номеру телефона",
    responses={
        404: {
            "description": "Номер телефона не найден",
            "content": {
                "application/json": {"example": {"detail": "Номер телефона не найден"}}
            },
        },
        500: {
            "description": "Удаление данных не удалось",
            "content": {
                "application/json": {
                    "example": {"detail": "Удаление данных не удалось"}
                }
            },
        },
    },
)
async def delete_address_phone(
    service: Annotated[StorageService, Depends(provide_storage_service)],
    phone: str = Path(description="Номер телефона для удаления"),
):
    try:
        service.delete_phone_address_info(phone)
        return {"detail": "Удаление успешно"}
    except PhoneNotFoundException:
        raise HTTPException(status_code=404, detail="Номер телефона не найден")
    except DeletionFailedException:
        raise HTTPException(status_code=500, detail="Удаление данных не удалось")
