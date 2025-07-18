from django.core.management.base import BaseCommand
from random import choice
from pages.models import Blog

class Command(BaseCommand):
    help = "Generate blogs"

    def handle(self, *args, **options):
        contents = [
            "To keep things simple for now, you can use the filesystem to store the articles. Each article will be stored as a separate file in a directory. The file will contain the title, content, and date of publication of the article. You can use JSON or Markdown format to store the articles.",

            "You can use any programming language to build the backend of the blog. You don’t have to make it as an API for this project, we have other projects for that. You can have pages that render the HTML directly from the server and forms that submit data to the server.",

            "For the frontend, you can use HTML and CSS (no need for JavaScript for now). You can use any templating engine to render the articles on the frontend.",
            "You can implement basic authentication for the admin section. You can either use the standard HTTP basic authentication or simply hardcode the username and password in the code for now and create a simple login page that will create a session for the admin."

        ]
        for i in range(0, 10):
            try:
                Blog.objects.create(
                    title=f"My first random blog {i}",
                    content=choice(contents)
                )
                self.stdout.write(self.style.SUCCESS(f"successfully created blog {i}"))
            except:
                self.stdout.write(self.style.ERROR(f"FAILED to created blog {i}"))
                raise
