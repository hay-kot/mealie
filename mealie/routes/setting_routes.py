from fastapi import APIRouter, HTTPException
from services.scheduler_services import post_webhooks
from services.settings_services import SiteSettings, SiteTheme
from utils.global_scheduler import scheduler
from utils.snackbar import SnackResponse

router = APIRouter(tags=["Settings"])


@router.get("/api/site-settings/")
def get_main_settings():
    """ Returns basic site settings """

    return SiteSettings.get_site_settings()


@router.post("/api/site-settings/webhooks/test/")
def test_webhooks():
    """ Run the function to test your webhooks """

    return post_webhooks()


@router.post("/api/site-settings/update/")
def update_settings(data: SiteSettings):
    """ Returns Site Settings """
    data.update()
    # try:
    #     data.update()
    # except:
    #     raise HTTPException(
    #         status_code=400, detail=SnackResponse.error("Unable to Save Settings")
    #     )

    scheduler.reschedule_webhooks()
    return SnackResponse.success("Settings Updated")


@router.get("/api/site-settings/themes/", tags=["Themes"])
def get_all_themes():
    """ Returns all site themes """

    return SiteTheme.get_all()


@router.get("/api/site-settings/themes/{theme_name}/", tags=["Themes"])
def get_single_theme(theme_name: str):
    """ Returns a named theme """
    return SiteTheme.get_by_name(theme_name)


@router.post("/api/site-settings/themes/create/", tags=["Themes"])
def create_theme(data: SiteTheme):
    """ Creates a site color theme database entry """
    data.save_to_db()
    # try:
    #     data.save_to_db()
    # except:
    #     raise HTTPException(
    #         status_code=400, detail=SnackResponse.error("Unable to Save Theme")
    #     )

    return SnackResponse.success("Theme Saved")


@router.post("/api/site-settings/themes/{theme_name}/update/", tags=["Themes"])
def update_theme(theme_name: str, data: SiteTheme):
    """ Update a theme database entry """
    data.update_document()

    # try:
    # except:
    #     raise HTTPException(
    #         status_code=400, detail=SnackResponse.error("Unable to Update Theme")
    #     )

    return SnackResponse.success("Theme Updated")


@router.delete("/api/site-settings/themes/{theme_name}/delete/", tags=["Themes"])
def delete_theme(theme_name: str):
    """ Deletes theme from the database """
    SiteTheme.delete_theme(theme_name)
    # try:
    #     SiteTheme.delete_theme(theme_name)
    # except:
    #     raise HTTPException(
    #         status_code=400, detail=SnackResponse.error("Unable to Delete Theme")
    #     )

    return SnackResponse.success("Theme Deleted")
