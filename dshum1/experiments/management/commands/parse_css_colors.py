from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection
from django.http import request
import requests
from bs4 import BeautifulSoup

from ...models import CssColor


class Command(BaseCommand):
    help = 'Parses w3schools.com and fills the database with css colors'

    def add_arguments(self, parser):
        parser.add_argument('--fake', action='store_true', default=False,
                            help='Fakes saving to database')
        parser.add_argument('--clean', action='store_true', default=False,
                            help='Cleans csscolor table before collecting data')

    def handle(self, *args, **options):
        if options['clean']:
            self.clean_table()

        url = "https://www.w3schools.com/colors/colors_groups.asp"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.title.string
        self.stdout.write(f"Title: {title}")

        existing_colors = CssColor.objects.all().values_list("keyword", flat=True)

        table = soup.find("table", class_="ws-table-all")
        shade = None
        added = exist = 0

        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            for td in tds:
                try:
                    col = int(td["colspan"])
                    if col == 5:
                        shade = td.text.lower().replace(" colors", "")
                except (ValueError, KeyError) as e:
                    pass
            if shade and len(tds) > 2:
                keyword = tds[0].text.strip().lower()
                hex_value = tds[1].text
                css_level = CssColor.get_css_level(keyword)

                if keyword not in existing_colors:
                    if not options['fake']:
                        CssColor.objects.create(
                            keyword=keyword,
                            hex_value=hex_value,
                            color_shade=shade,
                            css_level=css_level.value)
                    added += 1
                else:
                    exist += 1

        self.stdout.write(self.style.SUCCESS(f"Added colors: {added}"))
        self.stdout.write(self.style.SUCCESS(f"Existing colors: {exist}"))

    def clean_table(self):
        """Run django-admin sqlsequencereset app_label --database DATABASE to reset all tables"""
        CssColor.objects.all().delete()
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [CssColor])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        self.stdout.write(self.style.WARNING("Table csscolor has been cleaned"))
