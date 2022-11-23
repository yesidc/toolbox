from django.core.management.base import BaseCommand, CommandError
import glob
from tbcore.models import PlanCategoryOnlineIdea, OnlineIdea, Category
from tbcore.utils.base import Json5ParseException, InvalidDataException, CategoryDoesNotExist


# todo raise InvalidDataException if the directory (ideas or categories) contains no data
class Command(BaseCommand):
    help = "Reads json5 file and saves either ideas or categories/building blocks to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--save_idea',
            default=False,
            action='store_true',
            help='Save idea to the database',
        )

        parser.add_argument(
            '--save_category',
            default=False,
            action='store_true',
            help='Save category or building block to the database',
        )

    def handle(self, *args, **options):
        mode = None
        if options['save_idea']:
            mode = 'ideas'
        elif options['save_category']:
            mode = 'categories'

        if mode is None:
            raise Json5ParseException('Enter the required parameters: --save_category or --save_idea ')

        num_items_created = 0
        for filename in glob.glob("data/" + mode + "/*.json5"):
            with open(filename, "r", encoding="UTF-8") as f:
                data_json5 = f.read()

                try:
                    PlanCategoryOnlineIdea.check_json5(data_json5, mode)
                except Json5ParseException as e:
                    raise InvalidDataException("Data {} invalid. Error message: \n{}".format(filename, e))

                if mode == 'ideas':
                    if Category.objects.all():
                        OnlineIdea.create_from_json5(data_json5)
                    else:
                        raise CategoryDoesNotExist("First save the categories to the database. Use read_data --save_category")
                else:
                    Category.create_from_json5(data_json5)
                num_items_created += 1

        self.stdout.write(self.style.SUCCESS('Successfully created {} items.'.format(num_items_created)))
