import unittest

from basespace_commons.environment import Environment

class TestEnvironment(unittest.TestCase):
    Default = Environment(
            app_option_dict = {},
            sample_ids = ['id1', 'id2'],
            sample_names = ['name1', 'name2'],
            output_project_id = 'output_project_id',
            output_project_name = 'output_project_name',
            app_result_name = 'app_result_name',
            root_dir = 'root_dir'
            )

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
        env = TestEnvironment.Default
        self.assertListEqual(env.sample_names_and_ids(), [('name1', 'id1'), ('name2', 'id2')])
        self.assertEqual(env.output_project_id(), 'output_project_id')
        self.assertEqual(env.output_project_name(), 'output_project_name')
        self.assertEqual(env.app_result_name(), 'app_result_name')
        self.assertEqual(env.root_dir(), 'root_dir')
        self.assertEqual(env.output_project_dir(), 'root_dir/output/appresults/output_project_id/app_result_name')
        self.assertEqual(env.output_sample_dir('name2'), 'root_dir/output/appresults/output_project_id/app_result_name/name2')
        self.assertEqual(env.tmp_dir(), 'root_dir/scratch')
        self.assertEqual(env.num_samples(), 2)

    def test_fq_ext(self):
        self.assertEqual(Environment.fq_ext(end=1), "R1_001.fastq.gz")
        self.assertEqual(Environment.fq_ext(end=2), "R2_001.fastq.gz")
        with self.assertRaises(AssertionError):
            Environment.fq_ext(end=0)
        with self.assertRaises(AssertionError):
            Environment.fq_ext(end=3)

    # input_sample_dir() find at <root_dir>/input/samples/<sample_id>/Data/Intensities/Basecalls/
    # input_sample_dir() find at <root_dir>/input/samples/<sample_id>

    # input_sample_fastqs() sample name has underscores, replaced by dashes
    # input_sample_fastqs() fragment reads
    # input_sample_fastqs() paired reads
    # input_sample_fastqs() paired reads mismatching # of fastqs per end

    # from() handle app options with "Content"
    # from() handle app options with "Items"
    # from() handle input samples Input.BioSamples
    # from() handle input samples Input.sample-id
    # from() handle input samples Input.Samples
    # from() exception with missing input samples 

    # tests for add/set/get from the environment
