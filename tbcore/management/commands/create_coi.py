from django.core.management.base import BaseCommand, CommandError
from tbcore.models import CategoryOnlineIdea, Category, OnlineIdea

class Command(BaseCommand):
    help = 'Create CategoryOnline objects.'



    def handle(self, *args, **options):
        # create CategoryOnlineIdea objects

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Human Touch')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-as-014'),
            OnlineIdea.objects.get(idea_id='idea-hf-013'),
            OnlineIdea.objects.get(idea_id='idea-iv-015'),
            OnlineIdea.objects.get(idea_id='idea-pll-016')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Organization')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-s-020'),
            OnlineIdea.objects.get(idea_id='idea-stm-019'),
            OnlineIdea.objects.get(idea_id='idea-pe-018'),
            OnlineIdea.objects.get(idea_id='idea-ce-017')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assignments')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-rp-008'),
            OnlineIdea.objects.get(idea_id='idea-q-007'),
            OnlineIdea.objects.get(idea_id='idea-ps-006'),
            OnlineIdea.objects.get(idea_id='idea-pr-005')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Teaching Material')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-cm-024'),
            OnlineIdea.objects.get(idea_id='idea-cc-025'),
            OnlineIdea.objects.get(idea_id='idea-clo-026'),
            OnlineIdea.objects.get(idea_id='idea-ml-027')

        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Discussion')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-afm-009'),
            OnlineIdea.objects.get(idea_id='idea-sdt-010'),
            OnlineIdea.objects.get(idea_id='idea-pp-011'),
            OnlineIdea.objects.get(idea_id='idea-whops-012')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Student Engagement')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-af-020'),
            OnlineIdea.objects.get(idea_id='idea-or-022'),
            OnlineIdea.objects.get(idea_id='idea-q-007'),
            OnlineIdea.objects.get(idea_id='idea-sct-023')
        )

        CategoryOnlineIdea.objects.create(category=Category.objects.get(category_name='Assessment')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-ac-001'),
            OnlineIdea.objects.get(idea_id='idea-gr-002'),
            OnlineIdea.objects.get(idea_id='idea-oe-003'),
            OnlineIdea.objects.get(idea_id='idea-rpia-004')
        )

        CategoryOnlineIdea.objects.create(
            category=Category.objects.get(category_name='Rules & Regulations')).online_idea.add(
            OnlineIdea.objects.get(idea_id='idea-ac-001'),
            # todo add ideas for rules and regulations. These are not correct.
            OnlineIdea.objects.get(idea_id='idea-gr-002'),
            OnlineIdea.objects.get(idea_id='idea-oe-003'),
            OnlineIdea.objects.get(idea_id='idea-rpia-004')
        )

        self.stdout.write(self.style.SUCCESS('Successfully crated the CategoryOnline objects'))