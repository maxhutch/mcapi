import unittest
import tempfile
import filecmp
from os import environ
from os import remove
from os import path as os_path
from os.path import getsize, exists, isfile
from pathlib import Path
from mcapi import set_remote_config_url, get_remote_config_url, create_project
from mcapi import _create_file_with_upload, _download_data_to_file


remote_url = 'http://mctest.localhost/api'


class TestFileDownload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        set_remote_config_url(remote_url)
        cls.base_project_name = "FileUploadTest01"
        description = "Test project generated by automated test"
        project = create_project(cls.base_project_name, description)
        directory = project.get_top_directory()
        cls.base_project_id = project.id
        cls.base_project = project
        cls.base_directory_id = directory.id
        cls.base_directory = directory

    def test_is_setup_correctly(self):
        self.setup_test_files()
        self.assertEqual(get_remote_config_url(), remote_url)
        self.assertTrue(Path(self.make_test_dir_path('fractal.jpg')).is_file())
        self.assertTrue(Path(self.make_test_dir_path('NOEXT')).is_file())

        project = self.base_project
        self.assertIsNotNone(project)
        self.assertIsNotNone(project.name)
        self.assertEqual(self.base_project_name, project.name)
        self.assertIsNotNone(project.id)
        self.assertEqual(self.base_project_id, project.id)

        self.assertEqual(self.base_directory._project, self.base_project)

        self.assertIsNotNone(self.image_file)
        self.assertEqual(self.image_file.size, self.byte_count)
        self.assertEqual(self.image_file.name, self.image_file_name)

    def test_download_image_file_internal(self):
        self.setup_test_files()
        project = self.base_project
        test_file = self.image_file
        download_file_path = tempfile.gettempdir() + "/" + test_file.name
        if exists(download_file_path):
            remove(download_file_path)

        filepath = _download_data_to_file(project, test_file, download_file_path)

        self.assertTrue(exists(filepath))
        self.assertTrue(isfile(filepath))
        self.assertTrue(filecmp.cmp(self.make_test_dir_path('fractal.jpg'), filepath))

    def test_download_image_file_external(self):
        self.setup_test_files()
        project = self.base_project
        test_file = self.image_file
        download_file_path = tempfile.gettempdir() + "/" + test_file.name
        if exists(download_file_path):
            remove(download_file_path)

        filepath = test_file.download_file_content(download_file_path)

        self.assertTrue(exists(filepath))
        self.assertTrue(isfile(filepath))
        self.assertTrue(filecmp.cmp(self.make_test_dir_path('fractal.jpg'), filepath))

    def test_download_text_onext_file_internal(self):
        self.setup_test_files()
        project = self.base_project
        test_file = self.no_ext_file
        download_file_path = tempfile.gettempdir() + "/" + test_file.name
        if exists(download_file_path):
            remove(download_file_path)

        filepath = _download_data_to_file(project, test_file, download_file_path)

        self.assertTrue(exists(filepath))
        self.assertTrue(isfile(filepath))
        self.assertTrue(filecmp.cmp(self.make_test_dir_path('NOEXT'), filepath))

    def test_download_text_onext_file_external(self):
        self.setup_test_files()
        project = self.base_project
        test_file = self.no_ext_file
        download_file_path = tempfile.gettempdir() + "/" + test_file.name
        if exists(download_file_path):
            remove(download_file_path)

        filepath = test_file.download_file_content(download_file_path)

        self.assertTrue(exists(filepath))
        self.assertTrue(isfile(filepath))
        self.assertTrue(filecmp.cmp(self.make_test_dir_path('NOEXT'), filepath))

    def make_test_dir_path(self, file_name):
        self.assertTrue('TEST_DATA_DIR' in environ)
        test_path = os_path.abspath(environ['TEST_DATA_DIR'])
        self.assertIsNotNone(test_path)
        self.assertTrue(os_path.isdir(test_path))
        test_file = os_path.join(test_path, 'test_upload_data', file_name)
        self.assertTrue(os_path.isfile(test_file))
        return test_file

    def setup_test_files(self):
        if not hasattr(self, 'image_file_name'):
            path = Path(self.make_test_dir_path('fractal.jpg'))
            self.image_file_name = path.parts[-1]
            input_path = str(path.absolute())
            self.byte_count = getsize(input_path)
            self.image_file = _create_file_with_upload(self.base_project, self.base_directory, self.image_file_name, input_path)
        if not hasattr(self, 'no_ext_file_name'):
            path = Path(self.make_test_dir_path('NOEXT'))
            self.no_ext_file_name = path.parts[-1]
            input_path = str(path.absolute())
            self.no_ext_file_byte_count = getsize(input_path)
            self.no_ext_file = _create_file_with_upload(self.base_project, self.base_directory, self.no_ext_file_name, input_path)