import unittest
from random import randint
from mcapi import api
from mcapi import Remote
from mcapi import Config
from mcapi import create_project
from mcapi import Template

url = 'http://mctest.localhost/api'

def fake_name(prefix):
    number="%05d" % randint(0,99999)
    return prefix+number

class TestProcess(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        config = Config()
        api.set_remote(Remote(config=Config(config={'mcurl': url})))
        self.base_project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        self.base_project = create_project(self.base_project_name, description)
        self.base_project_id = self.base_project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        self.base_experiment = self.base_project.create_experiment(name, description)
        self.base_experiment_id = self.base_experiment.id

    def test_is_setup_correctly(self):
        self.assertEqual(api.use_remote().mcurl,url)
        self.assertIsNotNone(api.use_remote().config.params['apikey'])
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)
        self.assertIsNotNone(self.base_experiment)
        self.assertIsNotNone(self.base_experiment.id)
        self.assertEqual(self.base_experiment_id, self.base_experiment.id)

    def test_process_from_template_for_create_sample(self):
        process = self.base_experiment.create_process_from_template(Template.create)
        self.assertIsNotNone(process)
        self.assertIsNotNone(process.id)
        self.assertIsNotNone(process.process_type)
        self.assertEqual(process.process_type, 'create')
        self.assertTrue(process.does_transform)

    def test_process_from_template_for_computation(self):
        process = self.base_experiment.create_process_from_template(Template.compute)
        self.assertIsNotNone(process)
        self.assertIsNotNone(process.id)
        self.assertIsNotNone(process.process_type)
        self.assertEqual(process.process_type, 'analysis')
        self.assertFalse(process.does_transform)

