class MyPrintRouter(object):
    """
    A router to control all database operations on models in the
    build2myprint application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read build2myprint models go to MyPrint MSSQL DB.
        """
        if model._meta.app_label == 'build2myprint':
            return 'myprint'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes are only allowed on our database, not MyPrint's
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the build2myprint app.
        """
        if obj1._meta.app_label == 'build2myprint' and \
           obj2._meta.app_label == 'build2myprint':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the build2myprint models are not migrated nor managed by django in DB,
        as th DB already exists.
        """
        if app_label == 'build2myprint' or db == 'myprint':
            return False
        return None
