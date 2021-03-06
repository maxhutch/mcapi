import unittest
from random import randint
from os import environ
from os import path as os_path
from os.path import getsize
from pathlib import Path
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix + number


class TestFileMove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_name = fake_name("TestMoveProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.project_name, description)
        cls.project_id = project.id
        cls.project = project
        print ''
        print project.name

        cls.top_directory = project.get_top_directory()
        cls.test_dir_path_for_move = '/TestForMove'
        cls.directory_for_move = project.add_directory(cls.test_dir_path_for_move)
        cls.test_dir_path_a = "/TestForMove/A"
        cls.directory_a = project.add_directory(cls.test_dir_path_a)
        cls.test_dir_path_b = "/TestForMove/A/B"
        cls.directory_b = project.add_directory(cls.test_dir_path_b)
        cls.test_dir_path_c = "/TestForMove/A/B/C"
        cls.directory_c = project.add_directory(cls.test_dir_path_c)
        cls.test_dir_path_d = "/TestForMove/A/B/D"
        cls.directory_d = project.add_directory(cls.test_dir_path_d)
        cls.test_dir_path_e = "/TestForMove/A/E"
        cls.directory_e = project.add_directory(cls.test_dir_path_e)
        cls.test_dir_path_f = "/TestForMove/F"
        cls.directory_f = project.add_directory(cls.test_dir_path_f)

        cls.directory_for_file_move_name = "/FilesForMove"
        cls.directory_for_file_move = project.add_directory(cls.directory_for_file_move_name)
        if 'TEST_DATA_DIR' in environ:
            test_path = os_path.abspath(environ['TEST_DATA_DIR'])
            file_path = os_path.join(test_path, 'test_upload_data', 'fractal.jpg')
            path = Path(file_path)
            cls.file_path = str(path.absolute())
            cls.byte_count = getsize(file_path)
            cls.original_filename = "FileForMove.jpg"
            cls.test_file = project.add_file_using_directory(
                cls.directory_for_file_move,
                cls.original_filename,
                cls.file_path
            )
            cls.test_file_c = project.add_file_using_directory(
                cls.directory_c,
                cls.original_filename,
                cls.file_path
            )
            cls.test_file_d = project.add_file_using_directory(
                cls.directory_d,
                cls.original_filename,
                cls.file_path
            )

    def test_is_setup_correctly(self):
        self.assertTrue('TEST_DATA_DIR' in environ)
        self.assertIsNotNone(self.file_path)
        self.assertTrue(os_path.isfile(self.file_path))
        self.assertIsNotNone(self.test_file)
        self.assertEqual(self.test_file.size, self.byte_count)
        self.assertEqual(self.test_file.name, self.original_filename)

        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertEqual(self.top_directory.name, self.project.name)
        self.assertEqual(self.directory_a.name, self.project.name + self.test_dir_path_a)
        self.assertEqual(self.directory_b.name, self.project.name + self.test_dir_path_b)

        directory_list = self.project.get_all_directories()
        self.assertIsNotNone(directory_list)
        self.assertEqual(len(directory_list), 9)
        self.assertEqual(directory_list[0].name, self.project.name)
        self.assertEqual(directory_list[1].name, self.project.name + self.directory_for_file_move_name)
        self.assertEqual(directory_list[2].name, self.project.name + self.test_dir_path_for_move)
        self.assertEqual(directory_list[3].name, self.project.name + self.test_dir_path_a)
        self.assertEqual(directory_list[4].name, self.project.name + self.test_dir_path_b)
        self.assertEqual(directory_list[5].name, self.project.name + self.test_dir_path_c)
        self.assertEqual(directory_list[6].name, self.project.name + self.test_dir_path_d)
        self.assertEqual(directory_list[7].name, self.project.name + self.test_dir_path_e)
        self.assertEqual(directory_list[8].name, self.project.name + self.test_dir_path_f)

        file = self.test_file
        self.assertEqual(file._directory.id, self.directory_for_file_move.id)
        child_list = self.directory_for_file_move.get_children()
        probe = child_list[0]
        self.assertEqual(file.id,probe.id)
        self.assertEqual(file.name,probe.name)
        self.assertEqual(file._directory_id, probe._directory_id)
        self.assertEqual(file._directory_id, self.directory_for_file_move.id)

    def test_move_file(self):
        test_file = self.test_file
        target = self.directory_f
        updated_file = test_file.move(target)

        self.assertEqual(updated_file.id, test_file.id)
        self.assertEqual(updated_file._project, self.project)
        directory_list = self.project.get_directory_list(self.directory_for_file_move_name)
        directory = directory_list[-1]
        self.assertEqual(directory.id, self.directory_for_file_move.id)
        self.assertEqual(directory._project, self.project)
        child_list = directory.get_children()
        print(child_list)
        for child in child_list:
            print child.name

