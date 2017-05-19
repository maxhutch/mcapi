import unittest
import os
import re
import mcapi
from cli_test_functions import working_dir, captured_output, print_stringIO
from mcapi.cli.init import init_subcommand
from mcapi.cli.up import up_subcommand
from mcapi.cli.ls import ls_subcommand
from mcapi.cli.functions import make_local_project

url = 'http://mctest.localhost/api'

def mkdir_if(path):
    if not os.path.exists(path):
        os.mkdir(path)

def remove_if(path):
    if os.path.exists(path):
        os.remove(path)

def rmdir_if(path):
    if os.path.exists(path):
        os.rmdir(path)

def make_file(path, text):
    with open(path, 'w') as f:
        f.write(text)

class TestMCUp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mcapi.set_remote_config_url(url)
        if not 'TEST_DATA_DIR' in os.environ:
            raise Exception("No TEST_DATA_DIR environment variable")
        cls.cli_test_project_path = os.path.join(os.environ['TEST_DATA_DIR'], 'cli_test_project')
        cls.proj_path = os.path.join(cls.cli_test_project_path, 'CLITest')
        cls.dirs = [
          os.path.join(cls.proj_path, "level_1"),
          os.path.join(cls.proj_path, "level_1", "level_2")
        ]
        cls.files = [
          (os.path.join(cls.proj_path, "file_A.txt"), "This is file A, level 0"),
          (os.path.join(cls.proj_path, "file_B.txt"), "This is file B, level 0"),
          (os.path.join(cls.proj_path, "level_1", "file_A.txt"), "This is file A, level 1"),
          (os.path.join(cls.proj_path, "level_1", "file_B.txt"), "This is file B, level 1"),
          (os.path.join(cls.proj_path, "level_1", "level_2", "file_A.txt"), "This is file A, level 2"),
          (os.path.join(cls.proj_path, "level_1", "level_2", "file_B.txt"), "This is file B, level 2")
        ]
    
    @classmethod
    def init(cls):
        mkdir_if(cls.cli_test_project_path)
        mkdir_if(cls.proj_path)
        testargs = ['mc', 'init']
        with captured_output(testargs, wd=cls.proj_path) as (sout, serr):
            init_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        
        cls.make_test_files()
        
    
    @classmethod
    def clean_files(cls):
        cls.remove_test_files()
        mc = os.path.join(cls.proj_path, ".mc")
        config = os.path.join(mc, "config.json")
        remove_if(config)
        rmdir_if(mc)
        rmdir_if(cls.proj_path)
    
    @classmethod
    def clean_proj(cls):
        proj_list = mcapi.get_all_projects()
        proj_dict = {p.name:p for p in proj_list}
        if 'CLITest' in proj_dict:
            proj_dict['CLITest'].delete()

    @classmethod
    def clean(cls):
        cls.clean_proj()
        cls.clean_files()
    
    @classmethod
    def make_test_files(cls):
        for dir in cls.dirs:
            mkdir_if(dir)
        for val in cls.files:
            make_file(val[0], val[1])
    
    @classmethod
    def remove_test_files(cls):
        for val in cls.files:
            remove_if(val[0])
        for dir in reversed(cls.dirs):
            rmdir_if(dir)
    
    def setUp(self):
        self.clean()
        self.init()
    
    def tearDown(self):
        self.clean()
    
    def get_proj(self):
        return make_local_project(self.proj_path)

    def test_one_file(self):
        # ls 1 file (in top directory)
        testargs = ['mc', 'ls', self.files[2][0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[1].split()[4], 'file')
        self.assertEqual(out[1].split()[6], '-')
        self.assertEqual(out[1].split()[7], '-')
        self.assertEqual(out[1].split()[9], 'level_1/file_A.txt')
        self.assertEqual(out[1].split()[10], '-')
        
        testargs = ['mc', 'up', self.files[2][0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            up_subcommand()
        #print_stringIO(sout)
        
        testargs = ['mc', 'ls', self.files[2][0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[1].split()[4], 'file')
        self.assertNotEqual(out[1].split()[6], '-')
        self.assertEqual(out[1].split()[7], 'file')
        self.assertEqual(out[1].split()[9], 'level_1/file_A.txt')
        self.assertNotEqual(out[1].split()[10], '-')
        
    def test_one_dir(self):
        # ls directory
        testargs = ['mc', 'ls', self.dirs[0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[2].split()[4], 'file')
        self.assertEqual(out[2].split()[7], '-')
        self.assertEqual(out[3].split()[4], 'file')
        self.assertEqual(out[3].split()[7], '-')
        self.assertEqual(out[4].split()[4], 'dir')
        self.assertEqual(out[4].split()[7], '-')
        
        testargs = ['mc', 'up', self.files[2][0], self.files[3][0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            up_subcommand()
        #print_stringIO(sout)
        
        testargs = ['mc', 'ls', self.dirs[0]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[2].split()[4], 'file')
        self.assertNotEqual(out[2].split()[7], '-')
        self.assertEqual(out[3].split()[4], 'file')
        self.assertNotEqual(out[3].split()[7], '-')
        self.assertEqual(out[4].split()[4], 'dir')
        self.assertEqual(out[4].split()[7], '-')
    
    def test_two_dir(self):
        # ls two directories
        testargs = ['mc', 'ls', self.dirs[0], self.dirs[1]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[2].split()[4], 'file')
        self.assertEqual(out[2].split()[7], '-')
        self.assertEqual(out[3].split()[4], 'file')
        self.assertEqual(out[3].split()[7], '-')
        self.assertEqual(out[7].split()[4], 'file')
        self.assertEqual(out[7].split()[7], '-')
        self.assertEqual(out[8].split()[4], 'file')
        self.assertEqual(out[8].split()[7], '-')
        self.assertEqual(out[9].split()[4], 'dir')
        self.assertEqual(out[9].split()[7], '-')

        testargs = ['mc', 'up', self.dirs[1]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            up_subcommand()
        #print_stringIO(sout)
        
        testargs = ['mc', 'ls', self.dirs[0], self.dirs[1]]
        with captured_output(testargs, wd=self.proj_path) as (sout, serr):
            ls_subcommand()
        #print_stringIO(sout)
        out = sout.getvalue().splitlines()
        self.assertEqual(out[2].split()[4], 'file')
        self.assertNotEqual(out[2].split()[6], '-')
        self.assertEqual(out[2].split()[7], 'file')
        self.assertEqual(out[3].split()[4], 'file')
        self.assertNotEqual(out[3].split()[6], '-')
        self.assertEqual(out[3].split()[7], 'file')
        
        self.assertEqual(out[7].split()[4], 'file')
        self.assertEqual(out[7].split()[7], '-')
        self.assertEqual(out[8].split()[4], 'file')
        self.assertEqual(out[8].split()[7], '-')
        self.assertEqual(out[9].split()[4], 'dir')
        self.assertNotEqual(out[9].split()[6], '-')
        self.assertEqual(out[9].split()[7], 'dir')
    
    @classmethod
    def tearDownClass(cls):
        cls.clean()
        
            
