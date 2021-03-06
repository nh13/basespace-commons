"""This module implements a container for the BaseSpace environment.

* Environment container for the BaseSpace environment
"""

import sys
import json
from typing import Any, Dict, Iterator, List, Tuple
from pathlib import Path
from collections import MutableMapping, OrderedDict


class EnvironmentDefaults(object):

    DefaultRootDir = Path('/data')

class Environment(MutableMapping):
    """ Contains information for the given BaseSpace Environment. """

    def __init__(
        self,
        app_option_dict: Dict[str, Any],
        sample_ids: List[str],
        sample_names: List[str],
        output_project_id: str,
        output_project_name: str,
        app_result_name: str,
        root_dir: Path = EnvironmentDefaults.DefaultRootDir):
        """ Creates a a new environment. """
        assert len(sample_ids) == len(sample_names)
        self.__app_option_dict = app_option_dict
        self.__sample_ids = sample_ids
        self.__sample_names = sample_names
        self.__output_project_id = output_project_id
        self.__output_project_name = output_project_name
        self.__app_result_name = app_result_name
        self.__root_dir = root_dir

    def __getitem__(self, key: str) -> str:
        return self.__app_option_dict[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.__app_option_dict[key] = value

    def __delitem__(self, key: str) -> str:
        del self.__app_option_dict[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__app_option_dict.keys())

    def __len__(self) -> Iterator[str]:
        return len(self.__app_option_dict)

    @staticmethod
    def fq_ext(end: int=1) -> str:
        """ The file extension for the read <end> FASTQ. """
        assert end == 1 or end == 2
        return f"_R{end}_001.fastq.gz"

    def sample_names_and_ids(self) -> List[Tuple[str, str]]:
        """ Gets a the name and id foreach sample. """
        return list(zip(self.__sample_names, self.__sample_ids))

    def output_project_id(self) -> str:
        """ The output project identifier. """
        return self.__output_project_id

    def output_project_name(self) -> str:
        """ The output project name. """
        return self.__output_project_name

    def app_result_name(self) -> str:
        """ The name for the app result. """
        return self.__app_result_name

    def root_dir(self) -> Path:
        """ The root directory for all analyses. """
        return self.__root_dir

    def output_project_dir(self) -> Path:
        """ The path to the output project directory containing all the sample directories. """
        return self.root_dir() / 'output' / 'appresults' / self.output_project_id() / self.app_result_name()

    def output_sample_dir(self, sample_name: str) -> Path:
        """ The path to the output directory for the given sample. """
        return self.output_project_dir() / sample_name

    def tmp_dir(self) -> Path:
        """ The temporary directory to use for all analyses. """
        return self.root_dir() / 'scratch'

    def num_samples(self) -> int:
        """ Gets the number of samples. """
        return len(self.__sample_names)

    def input_sample_dir(self, sample_idx: int, try_alternate: bool=True) -> Path:
        """ Gets the path to the sample input directory containing the sample's FASTQ(s). """
        if len(self.__sample_ids) <= sample_idx or sample_idx < 0:
            raise Exception(f"Sample index '{sample_idx}' out of range (found {len(self.__sample_ids)} samples).")
        paths_tried = []
        path = self.root_dir() / 'input' / 'samples' / self.__sample_ids[sample_idx] / 'Data' / 'Intensities' / 'BaseCalls'
        paths_tried.append(path)
        if (not path.exists() or not path.is_dir()) and try_alternate:
            path = self.root_dir() / 'input' / 'samples' / self.__sample_ids[sample_idx]
            paths_tried.append(path)
        if not path.is_dir():
            raise Exception(f"Could not sample input directory for sample idx '{sample_idx}', tried paths:\n" + '\n'.join(['\t' + str(p) for p in paths_tried]))
        else:
            return path.resolve()

    def input_sample_fastqs(self, sample_idx: int) -> Tuple[List[Path], List[Path]]:
        """
        Gets the input sample FASTQ(s) for the ith sample.
        """
        sample_dir = self.input_sample_dir(sample_idx=sample_idx, try_alternate=True)

        # NB: basespace has a problem with underscores in basespace, as they are replaced with dashes
        sample_name = self.__sample_names[sample_idx].replace('_', '-')

        def get_fastqs(end: int) -> List[Path]:
            suffix = self.fq_ext(end=end)
            fastqs = [p.resolve() for p in sample_dir.iterdir() if p.name.endswith(suffix) and p.name.startswith(sample_name)]
            return [p for p in fastqs if p.exists() and p.is_file()]

        fastqs_r1 = get_fastqs(end=1)
        fastqs_r2 = get_fastqs(end=2)

        if len(fastqs_r1) == 0:
            raise Exception(f"No FASTQs found for R1 for sample '{sample_name}' in '{sample_dir}'.  Found:\n\t" + '\n\t'.join([f for f in sample_dir.iterdir() if f.is_file()]))
        elif len(fastqs_r2) > 0 and len(fastqs_r1) != len(fastqs_r2):
            raise Exception(f"Mismatching # of fastqs for R1 ({len(fastqs_r1)}) and R2 ({len(fastqs_r2)})")
        else:
            return (fastqs_r1, fastqs_r2)

    @staticmethod
    def from_json(app_session_json: Path, root_dir: Path=EnvironmentDefaults.DefaultRootDir) -> 'Environment':
        """
        Will read in the AppSession.json, parse out the input user App options (Properties -> Items),
        and configure the BaseSpace drive structure (i.e. environment).
        """

        # Read in the AppSession.json
        with app_session_json.open('r') as fh:
            json_data = json.loads(''.join(fh.readlines()), object_pairs_hook=OrderedDict)

        # Get the sub-set of the JSON that contains the App options given by the user
        app_option_dict = OrderedDict()
        for app_option in json_data['Properties']['Items']:
            name = app_option['Name']
            if 'Content' in app_option:
                value = app_option['Content']
                app_option_dict[name] = value
            elif 'Items' in app_option:
                value = app_option['Items']
                app_option_dict[name] = value

        # Get the input samples
        if 'Input.Samples' in app_option_dict:
            samples      = app_option_dict['Input.Samples']
            sample_ids   = [sample['Id'] for sample in samples]
            sample_names = [sample['Name'] for sample in samples]
        elif 'Input.sample-id' in app_option_dict:
            sample       = app_option_dict['Input.sample-id']
            sample_ids   = [sample['Id']]
            sample_names = [sample['Name']]
        elif 'Input.BioSamples' in app_option_dict:
            samples      = app_option_dict['Input.BioSamples']
            sample_ids   = [sample['Id'] for sample in samples]
            sample_names = [sample['UserSampleId'] for sample in samples]
        else:
            raise Exception('Could not find either Input.BioSamples or Input.sample-id key: ' + ', '.join(app_option_dict.keys()))

        return Environment(
                app_option_dict     = app_option_dict,
                sample_ids          = sample_ids,
                sample_names        = sample_names,
                output_project_id   = app_option_dict['Input.project-id']['Id'],
                output_project_name = app_option_dict['Input.project-id']['Name'],
                app_result_name     = json_data['Name'],
                root_dir            = root_dir
                )
