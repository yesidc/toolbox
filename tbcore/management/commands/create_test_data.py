from django.core.management.base import BaseCommand, CommandError
from tbcore.utils.base import InvalidDataException
from tbcore.utils import data


class Command(BaseCommand):
    help = "Creates n number of test data points"



    def add_arguments(self, parser):
        parser.add_argument('num_data_points', type=int)



    def handle(self, *args, **options):
        if 'num_data_points' in options:
            data.create_random_data(options['num_data_points'])
        else:
            raise InvalidDataException('Please specify a number of data points')

        self.stdout.write(self.style.SUCCESS('Data successfully created'))
