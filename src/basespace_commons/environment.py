"""This module implements a container for the BaseSpace environment. 

* Environment  container for the BaseSpace environment
"""

import os
import sys
import json
from collections import MutableMapping, OrderedDict


class EnvironmentDefaults(object):
    
    DefaultRootDir = "/data"



class Environment(MutableMapping):
    """ Contains information for the given BaseSpace Environment. """

    
    def __init__(self, app_option_dict, sample_ids, sample_names, output_project_id, output_project_name, app_result_name, root_dir=EnvironmentDefaults.DefaultRootDir):
        """ Creates a a new environment. """
        assert len(sample_ids) == len(sample_names)
        self.__app_option_dict = app_option_dict
        self.__sample_ids = sample_ids
        self.__sample_names = sample_names
        self.__output_project_id = output_project_id
        self.__output_project_name = output_project_name
        self.__app_result_name = app_result_name
        self.__root_dir = root_dir

    def __getitem__(self, key):
        return self.__app_option_dict[key]

    def __setitem__(self, key, value):
        self.__app_option_dict[key] = value

    def __delitem__(self, key):
        del self.__app_option_dict[key]

    def __iter__(self):
        return iter(self.__app_option_dict.keys())

    def __len__(self):
        return len(self.__app_option_dict)
  
    @staticmethod
    def fq_ext(end=1):
        """ The file extension for the read one FASTQ. """
        assert end == 1 or end == 2
        return f"R{end}_001.fastq.gz"

    def sample_names_and_ids(self):
        """ Gets a the name and id foreach sample. """
        return list(zip(self.__sample_names, self.__sample_ids))

    def output_project_id(self):
        """ The output project identifier. """
        return self.__output_project_id

    def output_project_name(self):
        """ The output project name. """
        return self.__output_project_name

    def app_result_name(self):
        """ The name for the app result. """
        return self.__app_result_name

    def root_dir(self):
        """ The root directory for all analyses. """
        return self.__root_dir
    
    def output_project_dir(self):
        """ The path to the output project directory containing all the sample directories. """
        return os.path.join(self.root_dir(), "output", "appresults", self.output_project_id(), self.app_result_name()) 

    def output_sample_dir(self, sample_name):
        """ The path to the output directory for the given sample. """
        return os.path.join(self.output_project_dir(), sample_name)
    
    def tmp_dir(self):
        """ The temporary directory to use for all analyses. """
        return os.path.join(self.root_dir(), "scratch")    

    def num_samples(self):
        """ Gets the number of samples. """
        return len(self.__sample_names)
    
    def input_sample_dir(self, sample_idx, try_alternate=True):
        """ Gets the path to the sample input directory containing the sample's FASTQ(s). """
        if len(self.__sample_ids) <= sample_idx or sample_idx < 0:
            raise Exception(f"Sample index '{sample_idx}' out of range (found {len(self.__sample_ids)} samples).")
        path = os.path.join(self.root_dir(), "input", "samples", self.__sample_ids[sample_idx], "Data", "Intensities", "BaseCalls")
        if (not os.path.exists(path) or not os.path.isdir(path)) and try_alternate:
            alt_path = os.path.join(self.root_dir(), "input", "samples", self.__sample_ids[sample_idx])
            if os.path.exists(alt_path) and os.path.isdir(alt_path):
                return alt_path
            else:
                raise Exception(f"Could not sample input directory for sample idx '{sample_idx}', tried paths:\n\t{path}\n\t{alt_path}\n")
        return path

    def input_sample_fastqs(self, sample_idx):
        """
        Gets the input sample FASTQ(s) for the ith sample.
        """
        sample_dir = self.input_sample_dir(sample_idx=sample_idx, try_alternate=True)
      
        # NB: basespace has a problem with underscores in basespace, as they are replaced with dashes 
        sample_name = self.__sample_names[sample_idx].replace("_", "-")
        
        def get_fastqs(which):
            suffix = self.fq_ext(which=which)
            fastqs = [os.path.join(sample_dir, f) for f in os.listdir(sample_dir) if f.endswith(suffix) and f.startswith(sample_name)]
            return [f for f in fastqs if os.path.exists(f) and os.path.isfile(f)] 

        fastqs_r1 = get_fastqs(which=1)
        fastqs_r2 = get_fastqs(which=2)

        if len(fastqs_r1) == 0:
            raise Exception(f"No FASTQs found for R1 for sample '{sample_name}' in '{sample_dir}'.  Found:\n\t" + "\n\t".join([f for f in os.listdir(sample_dir) if os.path.isfile(f)]))
        elif len(fastqs_r2) > 0 and len(fastqs_r1) != len(fastqs_r2):
            raise Exception(f"Mismatching # of fastqs for R1 ({len(fastqs_r1)}) and R2 ({len(fastqs_r2)})")
        else:
            return (fastqs_r1, fastqs_r2)

    @staticmethod
    def from_json(app_session_json, root_dir=EnvironmentDefaults.DefaultRootDir):
        """
        Will read in the AppSession.json, parse out the input user App options (Properties -> Items),
        and configure the BaseSpace drive structure (i.e. environment).
        """

        # Read in the AppSession.json
        fh = open(app_session_json, "r")
        json_data = json.loads("".join(fh.readlines()), object_pairs_hook=OrderedDict)
        fh.close()

        # Get the sub-set of the JSON that contains the App options given by the user
        app_option_dict = OrderedDict()
        for app_option in json_data["Properties"]["Items"]:
            name = app_option["Name"]
            if "Content" in app_option:
                value = app_option["Content"]
                app_option_dict[name] = value
            elif "Items" in app_option:
                value = app_option["Items"]
                app_option_dict[name] = value

        # Get the input samples
        if "Input.BioSamples" in app_option_dict:
            samples      = app_option_dict["Input.BioSamples"]
            sample_ids   = [sample["Id"] for sample in samples]
            sample_names = [sample["UserSampleId"] for sample in samples]
        elif "Input.sample-id" in app_option_dict:
            sample       = app_option_dict["Input.sample-id"]
            sample_ids   = [sample["Id"]]
            sample_names = [sample["Name"]]
        elif "Input.Samples" in app_option_dict:
            samples      = app_option_dict["Input.Samples"]
            sample_ids   = [sample["Id"] for sample in samples]
            sample_names = [sample["Name"] for sample in samples]
        else:
            raise Exception("Could not find either Input.BioSamples or Input.sample-id key: " + ", ".join(app_option_dict.keys()))

        return Environment(
                app_option_dict     = app_option_dict,
                sample_ids          = sample_ids,
                sample_names        = sample_names,
                output_project_id   = app_option_dict["Input.project-id"]["Id"],
                output_project_name = app_option_dict["Input.project-id"]["Name"],
                app_result_name     = json_data["Name"],
                root_dir            = root_dir
                )
