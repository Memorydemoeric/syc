from syc.settings import DATABASE_APPS_MAPPING


class MyRouter(object):
    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label in DATABASE_APPS_MAPPING:
            return db == DATABASE_APPS_MAPPING.get(app_label)
        else:
            return None