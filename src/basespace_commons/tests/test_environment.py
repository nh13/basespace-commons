import unittest
import tempfile
import os

from basespace_commons.environment import Environment

class TestEnvironment(unittest.TestCase):

    @staticmethod
    def build_default():
        root_dir = tempfile.mkdtemp(suffix='root_dir', prefix='tmp')
        env = Environment(
                app_option_dict = {'some-key' : 'some-value'},
                sample_ids = ['id1', 'id2'],
                sample_names = ['name1', 'name2'],
                output_project_id = 'output_project_id',
                output_project_name = 'output_project_name',
                app_result_name = 'app_result_name',
                root_dir = root_dir
                )
        return (env, root_dir)

    def test_init_ids_and_names_diff_length(self):
        with self.assertRaises(AssertionError):
            Environment(
                    app_option_dict = {},
                    sample_ids = ['id1', 'id2'],
                    sample_names = ['name1', 'name2', 'name3'],
                    output_project_id = 'output_project_id',
                    output_project_name = 'output_project_name',
                    app_result_name = 'app_result_name',
                    root_dir = 'root_dir'
                    )

    def test_init_ok(self):
        env, root_dir = TestEnvironment.build_default()
        self.assertListEqual(env.sample_names_and_ids(), [('name1', 'id1'), ('name2', 'id2')])
        self.assertEqual(env.output_project_id(), 'output_project_id')
        self.assertEqual(env.output_project_name(), 'output_project_name')
        self.assertEqual(env.app_result_name(), 'app_result_name')
        self.assertEqual(env.root_dir(), root_dir)
        self.assertEqual(env.output_project_dir(), root_dir + '/output/appresults/output_project_id/app_result_name')
        self.assertEqual(env.output_sample_dir('name2'), root_dir + '/output/appresults/output_project_id/app_result_name/name2')
        self.assertEqual(env.tmp_dir(), root_dir + '/scratch')
        self.assertEqual(env.num_samples(), 2)

    def test_fq_ext(self):
        self.assertEqual(Environment.fq_ext(end=1), "_R1_001.fastq.gz")
        self.assertEqual(Environment.fq_ext(end=2), "_R2_001.fastq.gz")
        with self.assertRaises(AssertionError):
            Environment.fq_ext(end=0)
        with self.assertRaises(AssertionError):
            Environment.fq_ext(end=3)

    def test_input_sample_dir(self):
        env, root_dir = TestEnvironment.build_default()
        sample_ids = [tup[1] for tup in env.sample_names_and_ids()]

        # requires <root_dir>/input/samples/<sample_id>/Data/Intensities/BaseCalls
        with self.assertRaises(Exception):
            env.input_sample_dir(sample_idx=0, try_alternate=False)
            env.input_sample_dir(sample_idx=1, try_alternate=False)

        # make sample directory for sample 0
        sample_dir = os.path.join(env.root_dir(), 'input', 'samples', sample_ids[0], 'Data', 'Intensities', 'BaseCalls')
        os.makedirs(sample_dir)
        self.assertEqual(env.input_sample_dir(sample_idx=0, try_alternate=False), sample_dir)
        with self.assertRaises(Exception):
            env.input_sample_dir(sample_idx=1, try_alternate=False)

        # make sample directory for sample 1, with alternate
        sample_dir = os.path.join(env.root_dir(), 'input', 'samples', sample_ids[1])
        os.makedirs(sample_dir)
        with self.assertRaises(Exception):
            env.input_sample_dir(sample_idx=1, try_alternate=False)
        self.assertEqual(env.input_sample_dir(sample_idx=1, try_alternate=True), sample_dir)

    def test_input_sample_fastqs(self):
        env, root_dir = TestEnvironment.build_default()
        for sample_idx, sample_name_and_id in enumerate(env.sample_names_and_ids()):
            sample_name, sample_id = sample_name_and_id
            sample_dir = os.path.join(env.root_dir(), 'input', 'samples', sample_id, 'Data', 'Intensities', 'BaseCalls')
            os.makedirs(sample_dir)
            
            f1 = os.path.join(sample_dir, sample_name + Environment.fq_ext(end=1))
            f2 = os.path.join(sample_dir, sample_name + Environment.fq_ext(end=2))
            
            # no FASTQs
            with self.assertRaises(Exception):
                env.input_sample_fastqs(sample_idx=sample_idx)

            # read one only
            with open(f1, 'w') as fh: fh.write("dummy")
            f1_actual, f2_actual = env.input_sample_fastqs(sample_idx=sample_idx)
            self.assertListEqual(f1_actual, [f1])
            self.assertListEqual(f2_actual, [])
            
            # read one and two
            with open(f2, 'w') as fh: fh.write("dummy")
            f1_actual, f2_actual = env.input_sample_fastqs(sample_idx=sample_idx)
            self.assertListEqual(f1_actual, [f1])
            self.assertListEqual(f2_actual, [f2])

            # read two has two FASTQs
            f2buggy = os.path.join(sample_dir, sample_name + ".buggy" + Environment.fq_ext(end=1))
            with open(f2buggy, 'w') as fh: fh.write("dummy")
            with self.assertRaises(Exception):
                env.input_sample_fastqs(sample_idx=sample_idx)
    
    # TODO: input_sample_fastqs() sample name has underscores, replaced by dashes

    # from() handle app options with "Content"
    # from() handle app options with "Items"
    # from() handle input samples Input.BioSamples
    # from() handle input samples Input.sample-id
    # from() handle input samples Input.Samples
    # from() exception with missing input samples 
    def test_from_json(self):

        pass

    # tests for set/get/del from the environment
    def test_get(self):
        env, root_dir = TestEnvironment.build_default()
        self.assertEqual(env['some-key'], 'some-value')
        with self.assertRaises(KeyError):
            env['does-not-exist']

    def test_set(self):
        env, root_dir = TestEnvironment.build_default()
        with self.assertRaises(KeyError):
            env['does-not-exist']
        env['does-not-exist'] = 'it-does-now'
        self.assertEqual(env['does-not-exist'], 'it-does-now')

    def test_del(self):
        env, root_dir = TestEnvironment.build_default()
        self.assertEqual(env['some-key'], 'some-value')
        env['some-key'] = 'new-value'
        self.assertEqual(env['some-key'], 'new-value')
