from django.core.management.base import BaseCommand
from blog.models import Tag, BlogPost

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create some tags
        tags = ['Django', 'Python', 'API', 'Development']
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        # Create some blog posts
        posts = [
            {'title': 'Getting Started with Django', 'content': 'This is a beginner\'s guide to Django.', 'category': 'Django'},
            {'title': 'Understanding REST APIs', 'content': 'This post explains the principles of REST APIs.', 'category': 'API'},
            {'title': 'Advanced Python Techniques', 'content': 'Explore advanced features of Python programming.', 'category': 'Python'},
        ]

        for post_data in posts:
            try:
                post_data['tags'] = Tag.objects.all()  # Assign all tags to each post
                if not BlogPost.objects.filter(title=post_data['title']).exists():
                    blog = BlogPost.objects.create(
                       title=post_data["title"],
                       content=post_data["content"],
                       category=post_data["category"],
                    )
                    blog.tags.set(post_data['tags'])
                    blog.save()

                    self.stdout.write(self.style.SUCCESS(f'Created {post_data["title"]} successfully'))
                else:
                    self.stdout.write(self.style.WARNING(f'Post "{post_data["title"]}" already exists, skipping.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error seeding post "{post_data["title"]}": {e}'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))