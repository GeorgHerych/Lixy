from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0008_dialogmessage"),
    ]

    operations = [
        migrations.AddField(
            model_name="dialogmessage",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
