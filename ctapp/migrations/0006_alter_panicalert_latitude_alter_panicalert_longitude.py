from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ctapp", "0005_alter_chatmessage_options_alter_chatroom_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="panicalert",
            name="latitude",
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name="panicalert",
            name="longitude",
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True),
        ),
    ]
