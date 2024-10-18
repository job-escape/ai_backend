import os

from django.contrib.auth.models import User
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps


def createsuperuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    """
    PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "Qwe707!")
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'admin')
    User.objects.create_superuser(ADMIN_NAME, password=PASSWORD_NAME.strip())


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]
    operations = [migrations.RunPython(createsuperuser)]