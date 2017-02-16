import argparse
from os import path as os_path
import demo_project as demo

def set_host_url_arg():
    parser.add_argument('--host', required=True,
                        help='the url for the Materials Commons server')
def set_datapath_arg():
    parser.add_argument('--datapath', required=True,
                        help='the path to the directory containing the files used by the build')
def set_apikey_arg():
    parser.add_argument('--apikey', required=True, help='rapikey for the user building the demo project')

parser = argparse.ArgumentParser(description='Build Demo Project.')
set_host_url_arg()
set_datapath_arg()
set_apikey_arg()

args = parser.parse_args()

host = args.host
path = os_path.abspath(args.datapath)
key = args.apikey

# log_messages
print "Running script to build demo project: "
print "  host = " + host + ", "
print "  key = " + key + ", "
print "  path = " + path

'''
if MCDB_PORT === 30815 and hostname == materialscommons.org then apihost = https://test.materialscommons.org
else if MCDB_PORT == 28015 and hostname == materialscommons.org then apihost = https://materialscommons.org
else if MCDB_PORT == 28015 and hostname = lift.something... then apihost = https://lift.materialscommons.org
else // we are on localhost so use mctest.localhost
'''

'''
$MCDIR/project_demo/files
'''