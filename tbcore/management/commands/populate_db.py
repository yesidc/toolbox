from django.core.management.base import BaseCommand, CommandError
from tbcore.models import  OnlineIdea, Category, CategoryOnlineIdea


class Command(BaseCommand):
    help = " Populates the CategoryOnlineIdea table with the correct information."
    def handle(self, *args, **options):
        CategoryOnlineIdea.populate_category_idea()

        self.stdout.write(self.style.SUCCESS('Successfully created items.'))
