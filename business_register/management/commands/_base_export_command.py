import os
from datetime import date
from django.conf import settings
from data_ocean import s3bucket
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from rest_framework.request import Request
from data_converter.file_generators import JSONGenerator, XMLGenerator


class BaseExportCommand(BaseCommand):
    help = 'Saves ALL PEPs data to file in "export/" directory'

    queryset = None
    select_related = []
    prefetch_related = []
    serializer_class = None
    file_code_name = ''

    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', type=str, default='xml', nargs='?', choices=['xml', 'json'])
        parser.add_argument('-l', '--limit', type=int, nargs='?')
        parser.add_argument('-p', '--pretty', dest='pretty', action='store_true')
        parser.add_argument('-s', '--s3', dest='s3', action='store_true')

    def print(self, message, success=False):
        if success:
            self.stdout.write(self.style.SUCCESS(f'> {message}'))
        else:
            self.stdout.write(f'> {message}')

    @staticmethod
    def get_export_dir():
        path = os.path.join(settings.BASE_DIR, 'export')
        os.makedirs(path, exist_ok=True)
        return path

    def save_to_file(self, file_name, data):
        self.print(f'Write to file - "export/{file_name}"')
        file_dir = self.get_export_dir()
        with open(os.path.join(file_dir, file_name), 'w') as file:
            file.write(data)
        return f'export/{file_name}'

    def handle(self, *args, **options):
        assert self.queryset
        assert self.serializer_class
        assert self.file_code_name

        export_format = options['format']
        pretty = options['pretty']
        limit = options['limit']
        export_to_s3 = options['s3']

        request = Request(HttpRequest())
        # request._request.GET.setdefault('show_check_companies', 'none')
        # request._request.GET.setdefault('company_relations', 'none')

        count = self.queryset.count()
        queryset = self.queryset.all()
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)
        if self.prefetch_related:
            queryset = queryset.prefetch_related(*self.prefetch_related)

        if limit:
            queryset = queryset[:limit]

        self.print(f'Start generate data in {export_format} format')
        if export_format == 'json':
            generator = JSONGenerator(indent=2 if pretty else None)
        elif export_format == 'xml':
            generator = XMLGenerator(pretty_print=pretty)
        else:
            raise ValueError(f'Format not allowed = "{export_format}"')

        generator.start()
        i = 1
        for obj in queryset.iterator():
            serializer = self.serializer_class(obj, context={'request': request})
            generator.add_list_item(serializer.data)
            if i % 10 == 0:
                self.stdout.write(f'Processed {i} of {count}', ending='\r')
            i += 1

        generator.finish()
        data = generator.get_data()

        file_name = f'dataocean_{self.file_code_name}_{date.today()}.{export_format}'
        if export_to_s3:
            url = s3bucket.save_file(f'{self.file_code_name}/{file_name}', data)
        else:
            url = self.save_to_file(file_name, data)

        self.print('Success!', success=True)
        self.print(url, success=True)
