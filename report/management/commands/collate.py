from report.utils import collate_results
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    '''Collate results for all the levels and positions'''
    help = 'Collate results for all the levels and positions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='clear all exisitng collations',
        )
        parser.add_argument(
            '--quiet',
            action='store_true',
            help='reduced reporting',
        )
        # parser.add_argument('-models', '--models', type=str, nargs='+', help='The model to run if empty, then all models will be populated')
        # parser.add_argument('-verbose', '--verbose', type=int, nargs='+', help='Run the population showing each line from the scripts')

    def handle(self, *args, **kwargs):

        # noisy or quiet
        is_verbose = True
        if kwargs['quiet']:
            is_verbose = False
            
        # clear collations
        can_clear = False
        if kwargs['clear']:
            can_clear = True

        # collate results
        total = collate_results(can_clear=can_clear, is_verbose=is_verbose)

        # display results
        self.stdout.write(self.style.SUCCESS(f'Collation completed! {total} total records collated.'))
