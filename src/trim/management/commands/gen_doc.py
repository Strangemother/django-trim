from django.core.management.base import BaseCommand, CommandError

from trim.models import django

# from polls.models import Question as Poll



class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    # parser.add_argument('poll_ids', nargs='+', type=int)

    # def handle(self, *args, **options):
    #     for poll_id in options['poll_ids']:
    #         try:
    #             poll = Poll.objects.get(pk=poll_id)
    #         except Poll.DoesNotExist:
    #             raise CommandError('Poll "%s" does not exist' % poll_id)

    #         poll.opened = False
    #         poll.save()

    #         self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))

    def handle(self, *args, **options):
        self.out("Handle gen doc")

    def out(self, *a):
        self.stdout.write(self.style.SUCCESS(" ".join(map(str, a))))
