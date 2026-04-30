import uuid

from django.db import migrations, models


def populate_uuids(apps, schema_editor):
    Solve = apps.get_model('cubi_web', 'Solve')
    for solve in Solve.objects.all():
        solve.solve_id = uuid.uuid4()
        solve.save(update_fields=['solve_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('cubi_web', '0003_alter_device_association_code'),
    ]

    operations = [
        # Step 1: Add solve_id as a nullable UUID field
        migrations.AddField(
            model_name='solve',
            name='solve_id',
            field=models.UUIDField(null=True),
        ),
        # Step 2: Populate UUIDs for existing rows
        migrations.RunPython(populate_uuids, migrations.RunPython.noop),
        # Step 3: Remove old PK
        migrations.RemoveField(
            model_name='solve',
            name='solve_no',
        ),
        # Step 4: Make solve_id non-null, unique, and the primary key
        migrations.AlterField(
            model_name='solve',
            name='solve_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
