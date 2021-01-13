from settings import USE_MONGO, USE_TINYDB

from db.db_base import BaseDocument
from db.db_setup import USE_MONGO, USE_TINYDB, tiny_db
from db.mongo.settings_models import SiteSettingsDocument, WebhooksDocument


class _Settings(BaseDocument):
    def __init__(self) -> None:

        self.primary_key = "name"

        if USE_TINYDB:
            self.store = tiny_db.settings

        self.document = SiteSettingsDocument

    def save_new(self, main: dict, webhooks: dict) -> str:

        if USE_MONGO:
            main["webhooks"] = WebhooksDocument(**webhooks)
            new_doc = self.document(**main)
            return new_doc.save()

        elif USE_TINYDB:
            main["webhooks"] = webhooks
            return self.store.save(main)

    def update(self, name: str, new_data: dict) -> dict:
        if USE_MONGO:
            document = self.document.objects.get(name=name)
            if document:
                document.update(set__webhooks=WebhooksDocument(**new_data["webhooks"]))
                document.save()
        elif USE_TINYDB:
            pass