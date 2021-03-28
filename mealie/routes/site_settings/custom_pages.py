from fastapi import APIRouter, Depends
from mealie.db.database import db
from mealie.db.db_setup import generate_session
from mealie.routes.deps import get_current_user
from mealie.schema.settings import CustomPageBase
from mealie.schema.snackbar import SnackResponse
from mealie.schema.user import UserInDB
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/api/site-settings/custom-pages", tags=["Settings"])


@router.get("")
def get_custom_pages(session: Session = Depends(generate_session)):
    """ Returns the sites custom pages """

    return db.custom_pages.get_all(session)


@router.post("")
async def create_new_page(
    new_page: CustomPageBase,
    session: Session = Depends(generate_session),
    current_user: UserInDB = Depends(get_current_user),
):
    """ Creates a new Custom Page """

    db.custom_pages.create(session, new_page.dict())

    return SnackResponse.success("New Page Created")


@router.get("/{id}")
async def delete_custom_page(
    id: int,
    session: Session = Depends(generate_session),
):
    """ Removes a custom page from the database """

    return db.custom_pages.get(session, id)


@router.delete("/{id}")
async def delete_custom_page(
    id: int,
    session: Session = Depends(generate_session),
    current_user: UserInDB = Depends(get_current_user),
):
    """ Removes a custom page from the database """

    db.custom_pages.delete(session, id)
    return
