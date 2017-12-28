import unittest

from basespace_commons import environment

class TestEnvironment(unittest.TestCase):
    # Tests to write

    # fq_ext()
    
    # output_project_id()

    # output_project_name()

    # app_result_name()

    # root_dir()

    # input_sample_dir() find at <root_dir>/input/samples/<sample_id>/Data/Intensities/Basecalls/
    # input_sample_dir() find at <root_dir>/input/samples/<sample_id>

    # input_sample_fastqs() sample name has underscores, replaced by dashes
    # input_sample_fastqs() fragment reads
    # input_sample_fastqs() paired reads
    # input_sample_fastqs() paired reads mismatching # of fastqs per end

    # output_project_id()
    # output_project_name()

    # output_project_dir() find at <root_dir>/output/appresults/<project-id>/<app_result_name>
    # output_sample_dir() find at <root_dir>/output/appresults/<project-id>/<app_result_name>/<sample-name>
    # tmp_dir()find at <root_dir>/scratch

    # from() handle app options with "Content"
    # from() handle app options with "Items"
    # from() handle input samples Input.BioSamples
    # from() handle input samples Input.sample-id
    # from() handle input samples Input.Samples
    # from() exception with missing input samples 
    
    pass
