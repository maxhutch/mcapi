import unittest
from mcapi import set_remote_config_url
from cli_test_functions import captured_output, print_stringIO
from mcapi.cli.proj import ProjSubcommand

url = 'http://mctest.localhost/api'

class TestMCProj(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_remote_config_url(url)
        cls.proj_subcommand = ProjSubcommand()
    
    def test_mc_proj(self):
        testargs = ['mc', 'proj']
        with captured_output() as (sout, serr):
            self.proj_subcommand(testargs)
        print_stringIO(sout)
        out = sout.getvalue().splitlines()
        err = serr.getvalue().splitlines()
        
        headers = out[0].split()
        self.assertEqual(headers[0], "name")
        self.assertEqual(headers[1], "owner")
        self.assertEqual(headers[2], "id")
            
            