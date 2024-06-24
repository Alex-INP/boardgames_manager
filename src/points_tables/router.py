from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from .models import Template
from .schemas import TemplateBase
from src.dependencies import get_session


router = APIRouter()


@router.get("/create_header")
async def create_header(
    request: Request, template: TemplateBase, db: Session = Depends(get_session)
):
    tmpl_obj = Template(name=template.name)

    db.add(tmpl_obj)
    db.commit()

    fetched_header = db.query(Template).filter(Template.name == tmpl_obj.name).first()
    return fetched_header.name
