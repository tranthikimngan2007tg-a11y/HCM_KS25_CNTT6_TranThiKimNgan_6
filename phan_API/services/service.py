from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.database import get_db
from models.model import Department, Service
from schemas.schema import ServiceCreate, ServiceResponse


router = APIRouter()


@router.get("/services", response_model=list[ServiceResponse])
def list_services(db: Session = Depends(get_db)) -> list[Service]:
    return db.query(Service).order_by(Service.id).all()


@router.post(
    "/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    service: ServiceCreate, db: Session = Depends(get_db)
) -> Service:
    if db.get(Department, service.department_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    db_service = Service(**service.model_dump())
    db.add(db_service)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A service with this service_code already exists",
        ) from exc

    db.refresh(db_service)
    return db_service


@router.delete(
    "/departments/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_department(
    department_id: int, db: Session = Depends(get_db)
) -> Response:
    department = db.get(Department, department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    db.delete(department)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete a department that has services",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)