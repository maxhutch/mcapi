import unittest
import pytest
from random import randint
from mcapi import create_project, Template


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number

class TestMeasurementSetup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project_name = fake_name("TestMeasurementSetupProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(cls.project_name, description)
        cls.project_id = cls.project.id
        name = "TestMeasurementSetup"
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(name, description)
        cls.experiment_id = cls.experiment.id
        cls.process = cls.experiment.create_process_from_template(Template.primitive_crystal_structure)
        cls.sample_name = "setup-sample-1"
        cls.samples = cls.process.create_samples(sample_names=[cls.sample_name])
        cls.sample = cls.samples[0]

    def test_is_setup_correctly(self):
        self.assertIsNotNone(self.project)
        self.assertIsNotNone(self.project.name)
        self.assertEqual(self.project_name, self.project.name)
        self.assertIsNotNone(self.project.id)
        self.assertEqual(self.project_id, self.project.id)
        self.assertIsNotNone(self.experiment)
        self.assertIsNotNone(self.experiment.id)
        self.assertEqual(self.experiment_id, self.experiment.id)
        self.assertIsNotNone(self.process)
        self.assertIsNotNone(self.process.id)
        self.assertIsNotNone(self.process.process_type)
        self.assertEqual(self.process.process_type, 'create')
        self.assertTrue(self.process.does_transform)
        sample = self.sample
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.name)
        self.assertIsNotNone(sample.property_set_id)
        self.assertEqual(sample.name, self.sample_name)

    def test_fetch_sample_by_id(self):
        fetched_sample = self.project.fetch_sample_by_id(self.sample.id)
        self.assertIsNotNone(fetched_sample)
        self.assertIsNotNone(fetched_sample.processes)
        self.assertEqual(len(fetched_sample.processes),1)
        process = fetched_sample.processes[0]
        self.assertIsNotNone(process.input_data['property_set_id'])
        self.assertIsNotNone(process.property_set_id)
        self.assertEqual(process.input_data['property_set_id'],process.property_set_id)

    def test_process_list_of_samples_and_property_sets(self):
        process = self.process
        self.assertIsNotNone(process.output_samples)
        self.assertEqual(len(process.output_samples),1)
        self.assertEqual(process.output_samples[0].id,self.sample.id)
        samples = process.output_samples
        list = process.make_list_of_samples_with_property_set_ids(samples)
        self.assertTrue(len(list), 1)
        self.assertIsNotNone(list[0]['property_set_id'])
        self.assertIsNotNone(list[0]['sample'])
        self.assertIsNotNone(list[0]['sample'].id)
        self.assertIsNotNone(list[0]['sample'].name)
        self.assertEqual(list[0]['sample'].id, self.sample.id)
        self.assertEqual(list[0]['sample'].name, self.sample.name)

