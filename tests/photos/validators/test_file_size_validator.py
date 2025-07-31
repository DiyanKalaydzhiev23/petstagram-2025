from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from photos.validators import FileSizeValidator


class TestFileSizeValidator(TestCase):
    def setUp(self):
        self.max_size = 5
        self.max_size_in_mb = self.max_size * 1024 * 1024
        self.message = "Custom message"
        self.validator = FileSizeValidator(
            file_size_limit=self.max_size,
            message=self.message,
        )

    def test_valid_file_size_expect_no_errors(self):
        file = SimpleUploadedFile(
            'good.txt',
            b"a" * self.max_size_in_mb
        )

        try:
            self.validator(file)
        except ValidationError:
            self.fail('File size was correct. No fail expected.')

    def test_upload_more_than_max_size_raises_validation_error(self):
        file = SimpleUploadedFile(
            'good.txt',
            b"a" * (self.max_size_in_mb + 1)
        )

        with self.assertRaises(ValidationError) as ve:
            self.validator(file)

        self.assertEqual(self.message, ve.exception.message)