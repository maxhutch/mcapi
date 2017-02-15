import unittest
from random import randint
from mcapi import set_remote_config_url
from mcapi import create_project, Template
from casm_mcapi import _set_measurement


url = 'http://mctest.localhost/api'


def fake_name(prefix):
    number = "%05d" % randint(0, 99999)
    return prefix+number


class TestSetMeasurement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_remote_config_url(url)
        cls.project_name = fake_name("TestProject-")
        description = "Test project generated by automated test"
        cls.project = create_project(cls.project_name, description)
        cls.project_id = cls.project.id
        name = fake_name("TestExperiment-")
        description = "Test experiment generated by automated test"
        cls.experiment = cls.project.create_experiment(name, description)
        cls.experiment_id = cls.experiment.id
        cls.process = cls.experiment.create_process_from_template(
            Template.primitive_crystal_structure)
        cls.sample_name = "pcs-sample-1"
        cls.sample = cls.process.create_samples(
            sample_names=[cls.sample_name]
        )[0]

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
        samples = self.process.output_samples
        self.assertIsNotNone(sample)
        self.assertIsNotNone(sample.name)
        self.assertIsNotNone(sample.property_set_id)
        self.assertEqual(sample.name, self.sample_name)
        self.assertEqual(sample.name, samples[0].name)

    def test_measurement_attribute_name(self):
        value = "Test Primitive Crystal Structure"
        data = {"name":"Name",
            "attribute":"name",
            "otype":"string",
            "unit":"",
            "units": [],
            "value":value,
            "is_best_measure":True}
        measurement = self.process.create_measurement(data=data)
        self.assertEqual(measurement.name,"Name")
        self.assertEqual(measurement.attribute,"name")
        self.assertEqual(measurement.otype,"string")
        self.assertEqual(measurement.unit,"")
        self.assertEqual(measurement.value,value)

    def test_inline_pretest_set_measurement_basic(self):
        attribute = "name"
        measurement_name = "Name"
        measurement_value = "test value for attribute"
        measurement_data = {
            "name": measurement_name,
            "attribute": attribute,
            "otype": "string",
            "unit":"",
            "units": [],
            "value": measurement_value,
            "is_best_measure": True
            }
        measurement_property = {
            "name": measurement_name,
            "attribute": attribute
        }
        process = self.process
        measurement = process.create_measurement(data=measurement_data)
        self.assertEqual(measurement.name,measurement_name)
        self.assertEqual(measurement.attribute,attribute)
        self.assertEqual(measurement.otype,"string")
        self.assertEqual(measurement.unit,"")
        self.assertEqual(measurement.value,measurement_value)
        process_out = process.set_measurements_for_process_samples(
            measurement_property, [measurement])
        sample_out = process_out.output_samples[0]
        properties_out = sample_out.properties
        measurement_out = properties_out[0].best_measure[0]
        self.assertEqual(measurement_out.name, measurement_name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "string")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value, measurement_value)

    def test_set_measurement_basic(self):
        attribute = "name"
        measurement_name = "Name"
        measurement_value = "test value for attribute"
        measurement_data = {
            "name": measurement_name,
            "attribute": attribute,
            "otype": "string",
            "unit":"",
            "units": [],
            "value": measurement_value,
            "is_best_measure": True
            }
        process = _set_measurement(
               self.process, attribute, measurement_data, measurement_name)
        sample_out = process.output_samples[0]
        properties_out = sample_out.properties
        measurement_out = properties_out[0].best_measure[0]
        self.assertEqual(measurement_out.name, measurement_name)
        self.assertEqual(measurement_out.attribute, attribute)
        self.assertEqual(measurement_out.otype, "string")
        self.assertEqual(measurement_out.unit, "")
        self.assertEqual(measurement_out.value, measurement_value)
