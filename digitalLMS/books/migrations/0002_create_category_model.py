# Generated manually for category migration
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        # Step 1: Create Category model
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the category name (e.g., Programming, Fiction)', max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of this category')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the category was created')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        # Step 2: Rename old category field
        migrations.RenameField(
            model_name='book',
            old_name='category',
            new_name='category_old',
        ),
        # Step 3: Add new ForeignKey field (nullable temporarily)
        migrations.AddField(
            model_name='book',
            name='category_new',
            field=models.ForeignKey(
                null=True,
                blank=True,
                help_text='Select the book category',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='books',
                to='books.category'
            ),
        ),
    ]
