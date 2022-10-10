from django.core.management.base import BaseCommand, CommandError
import glob
from tbcore.models import OnlineIdea

class Command(BaseCommand):

   help = "Reads json5 file and saves idea's information to the database"
   def handle(self, *args, **options):
        num_ideas_created = 0
        for filename in glob.glob("data/ideas/idea_*.json5"):
            with open(filename, "r", encoding="UTF-8") as f:
                idea_json5 = f.read()
                OnlineIdea.create_from_json5(idea_json5)
                num_ideas_created += 1

        self.stdout.write(self.style.SUCCESS('Successfully created {} ideas.'.format(num_ideas_created)))