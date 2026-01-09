# test for trim/models/django.py
import unittest

from django.db import models

from trim.models import fields


class DjangoFieldsTestCase(unittest.TestCase):
    def test_types(self):
        """Test that the URL field is correctly registered."""
        names = {
            "url": models.URLField,
            "text": models.TextField,
            "chars": models.CharField,
            "email": models.EmailField,
            "integer": models.IntegerField,
            "boolean": models.BooleanField,
            "date": models.DateField,
            "datetime": models.DateTimeField,
            "time": models.TimeField,
            "decimal": models.DecimalField,
            "float": models.FloatField,
            "filepath": models.FilePathField,
            "binary": models.BinaryField,
            "slug": models.SlugField,
            "ip_addr": models.GenericIPAddressField,
            "pos_int": models.PositiveIntegerField,
            "pos_small_int": models.PositiveSmallIntegerField,
            "small_int": models.SmallIntegerField,
            "big_int": models.BigIntegerField,
            "null_bool": models.BooleanField,
            "duration": models.DurationField,
            "json": models.JSONField,
            "uuid": models.UUIDField,
            # "fk": models.ForeignKey,
            "rand_str": models.CharField,
            "null_bool": models.BooleanField,
            "true_bool": models.BooleanField,
            "false_bool": models.BooleanField,
            "blank_dt": models.DateTimeField,
            "dt_created": models.DateTimeField,
            "dt_updated": models.DateTimeField,
            # "dt_cu_pair"
            # user_fk
            # self_fk
            # m2m
            # self_m2m
            # o2o
            # user_o2o
            # user_m2m
            # image
            # auto
            # big_auto
            # decimal
            # duration
            # file
            # float_
            # pos_big_int
            # slug
            # small_auto
            # small_int
            # uuid_null
            # pk_uuid
            # str_uuid
        }
        """Synonymous to:
            self.assertIsInstance(fields.boolean(), models.BooleanField)
        """
        for name, field_type in names.items():
            with self.subTest(name=name):
                field = getattr(fields, name)()
                self.assertIsInstance(field, field_type)
