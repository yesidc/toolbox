from django.core.management.base import BaseCommand, CommandError
from tbcore.models import CategoryOnlineIdea, Category, OnlineIdea

class Command(BaseCommand):
    help = 'Create CategoryOnline objects.'



    def handle(self, *args, **options):
        # create CategoryOnlineIdea objects

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Human Touch')).online_idea.add(
            OnlineIdea.objects.get(idea_id='014-idea-as'),
            OnlineIdea.objects.get(idea_id='013-idea-hf'),
            OnlineIdea.objects.get(idea_id='015-idea-iv'),
            OnlineIdea.objects.get(idea_id='016-idea-pll')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Organization')).online_idea.add(
            OnlineIdea.objects.get(idea_id='020-idea-s'),
            OnlineIdea.objects.get(idea_id='019-idea-stm'),
            OnlineIdea.objects.get(idea_id='018-idea-pe'),
            OnlineIdea.objects.get(idea_id='017-idea-ce')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assignments')).online_idea.add(
            OnlineIdea.objects.get(idea_id='008-idea-rp'),
            OnlineIdea.objects.get(idea_id='007-idea-q'),
            OnlineIdea.objects.get(idea_id='006-idea-ps'),
            OnlineIdea.objects.get(idea_id='005-idea-pr')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Teaching Material')).online_idea.add(
            OnlineIdea.objects.get(idea_id='024-idea-cm'),
            OnlineIdea.objects.get(idea_id='025-idea-cc'),
            OnlineIdea.objects.get(idea_id='026-idea-clo'),
            OnlineIdea.objects.get(idea_id='027-idea-ml')

        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Discussion')).online_idea.add(
            OnlineIdea.objects.get(idea_id='009-idea-afm'),
            OnlineIdea.objects.get(idea_id='010-idea-sdt'),
            OnlineIdea.objects.get(idea_id='011-idea-pp'),
            OnlineIdea.objects.get(idea_id='012-idea-whops')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Student Engagement')).online_idea.add(
            OnlineIdea.objects.get(idea_id='021-idea-af'),
            OnlineIdea.objects.get(idea_id='022-idea-or'),
            OnlineIdea.objects.get(idea_id='007-idea-q'),
            OnlineIdea.objects.get(idea_id='023-idea-sct')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assessment')).online_idea.add(
            OnlineIdea.objects.get(idea_id='001-idea-ac'),
            OnlineIdea.objects.get(idea_id='002-idea-gr'),
            OnlineIdea.objects.get(idea_id='003-idea-oe'),
            OnlineIdea.objects.get(idea_id='004-idea-rpia')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Rules & Regulations')).online_idea.add(
            OnlineIdea.objects.get(idea_id='001-idea-ac'),
            # todo add ideas for rules and regulations. These are not correct.
            OnlineIdea.objects.get(idea_id='002-idea-gr'),
            OnlineIdea.objects.get(idea_id='003-idea-oe'),
            OnlineIdea.objects.get(idea_id='004-idea-rpia')
        )

        self.stdout.write(self.style.SUCCESS('Successfully crated the CategoryOnline objects'))