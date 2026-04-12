from django.core.management.base import BaseCommand
from web.models import TeamMember

class Command(BaseCommand):
    help = 'Seeds team members'

    def handle(self, *args, **kwargs):
        TeamMember.objects.all().delete()
        
        team_members = [
            {
                'name': 'Sarah Chen',
                'role': 'Chief Executive Officer',
                'bio': 'With over 15 years in the automotive industry, Sarah leads Turbo with a vision for innovation and customer satisfaction.',
            },
            {
                'name': 'Marcus Rodriguez',
                'role': 'Head of Sales',
                'bio': 'Marcus brings energy and expertise to our sales team, ensuring every customer finds their perfect match.',
            },
            {
                'name': 'David Kim',
                'role': 'Service Director',
                'bio': 'A certified master mechanic, David oversees our state-of-the-art service center with precision and care.',
            }
        ]

        for member in team_members:
            TeamMember.objects.create(**member)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded team members'))
