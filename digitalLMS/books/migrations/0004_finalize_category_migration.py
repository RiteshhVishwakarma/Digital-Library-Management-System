# Final migration to clean up category fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_migrate_category_data'),
    ]

    operations = [
        # Step 1: Remove old category field
        migrations.RemoveField(
            model_name='book',
            name='category_old',
        ),
        # Step 2: Rename new field to category
        migrations.RenameField(
            model_name='book',
            old_name='category_new',
            new_name='category',
        ),
        # Step 3: Make category field non-nullable
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(
                help_text='Select the book category',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='books',
                to='books.category'
            ),
        ),
    ]
