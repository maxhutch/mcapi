import unittest
from random import randint
from mcapi import api
from mcapi import create_project


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestExperiment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        project = create_project(cls.base_project_name, description)
        cls.base_project_id = project.id
        cls.base_project = project

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.base_project)
        self.assertIsNotNone(self.base_project.name)
        self.assertEqual(self.base_project_name, self.base_project.name)
        self.assertIsNotNone(self.base_project.id)
        self.assertEqual(self.base_project_id, self.base_project.id)

    def test_create_experiment_api(self):
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        obj = api.create_experiment(self.base_project_id, name, description)
        self.assertIsNotNone(obj)
        self.assertEqual(obj['otype'], 'experiment')

    def test_create_project_object(self):
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        experiment = self.base_project.create_experiment(name, description)
        self.assertIsNotNone(experiment.id)
        self.assertIsNotNone(experiment.name)
        self.assertEqual(name, experiment.name)
        self.assertIsNotNone(experiment.description)
        self.assertEqual(description, experiment.description)

    def test_get_experiment(self):
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        experiment = self.base_project.create_experiment(name, description)
        experiments = self.base_project.get_all_experiments()
        found_experiment = None
        for ex in experiments:
            if ex.id == experiment.id:
                found_experiment = ex
        self.assertIsNotNone(found_experiment)
        self.assertIsNotNone(found_experiment.name)
        self.assertEqual(name, found_experiment.name)
