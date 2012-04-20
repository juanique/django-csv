from django.test import TestCase
from testing.models import Country, City
from csv import CSVImporter, CSVImporterMapping

class BasicTestCase(TestCase):

    def test_suite(self):
        self.assertEquals(1 + 1, 2)

    def test_basic(self):
        """It can be initialized with a given separator and a mapping.
        it loads a data file and read its headers."""

        importer = CSVImporter(separator=" ", mapping=None)
        importer.open("fixtures/test_1.csv")
        self.assertEquals(['country.name', 'city.name'], importer._headers)

class MappingTestCase(TestCase):

    def setUp(self):
        self.mapping = CSVImporterMapping()
        self.importer = CSVImporter(separator=" ", mapping=self.mapping)
        self.importer.open("fixtures/test_1.csv")

    def test_mapping(self):
        """It receives a mapping of classes"""

        self.mapping.map_class('country', Country)
        self.mapping.map_class('city', City)

    def test_mapping_relations(self):
        """Relations can be defined"""

        self.mapping.map_relation(base="city", attribute="country", target="country")


class ReadTestCase(TestCase):

    def setUp(self):
        self.mapping = CSVImporterMapping()
        self.mapping.map_class('country', Country)
        self.mapping.map_class('city', City)

        self.importer = CSVImporter(separator=" ", mapping=self.mapping)
        self.importer.open("fixtures/test_1.csv")


    def test_readline(self):
        """It can read a line and construct the corresponding models"""

        results = self.importer.readline()
        results['country'].__class__ == Country
        results['city'].__class__ == City

    def test_relation(self):
        """It can establish relationships betweeen models on the same line."""

        self.mapping.map_relation(base="city", attribute="country", target="country")

        results = self.importer.readline()
        self.assertEqual(results['city'].country, results['country'])

    def test_save(self):
        """It can save the parsed result to the DB."""

        self.mapping.map_relation(base="city", attribute="country", target="country")

        results = self.importer.readline()
        self.importer.save_row(results)

        for name, obj in results.items():
            self.assertNotEquals(None, obj.pk)
