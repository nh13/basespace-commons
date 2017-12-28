"""This module implements a container for a sample. """

import os
import sys
import csv
from collections import OrderedDict
from basespace_commons import Environment

class Sample:
    """ Stores information about a sample. """

    def __init__(self, sample_dict, sample_ordinal):
        """ Creates a new sample with metadata in key-value pairs, and a given sample ordinal. Both
            the 'sample_name' and 'sample_id' keys should be defined.
        """
        self.__dict = sample_dict
        self.__sample_ordinal = sample_ordinal
        assert 'sample_name' in sample_dict
        assert 'sample_id' in sample_dict
        assert 0 < self.__sample_ordinal

    def bam(self, dir, ext="bam", unmatched=False, illumina_naming=False, sample_barcode_column=None):
        """
        Returns the output BAM file name produced by fgbio's DemuxFastqs. 

        See prefix() for how the file prefix will be generated.
        """
        prefix = self.prefix(unmatched=unmatched, illumina_naming=illumina_naming, sample_barcode_column=sample_barcode_column)
        return os.path.join(dir, f"{prefix}.{ext}")

        return os.path.join(dir, f"{sample_name}_S{self.__sample_ordinal:d}_L001.{ext}")

    def fq(self, dir, end, unmatched=None,illumina_naming=False, sample_barcode_column=None):
        """
        Returns the output FASTQ file name produced by fgbio's DemuxFastqs. 
        
        See prefix() for how the file prefix will be generated.

        The file extension will be "_R1_001.fastq.gz" when end is 1, or "_R2_001.fastq.gz"
        when end is 2.
        """
        assert 1 == end or 2 == end 
        ext = Environment.fq_ext(end=end)
        prefix = self.prefix(unmatched=unmatched, illumina_naming=illumina_naming, sample_barcode_column=sample_barcode_column)
        return os.path.join(dir, f"{prefix}.{ext}")

    def prefix(self, unmatched=False, illumina_naming=False, sample_barcode_column=None):
        """
        Returns the output file name produced by fgbio's DemuxFastqs. 

        If illumina_naming is True, then the output file prefix will be:
            <sample-name>_S<sample_ordinal>_L001
        Otherwise, the prefix will be the concatenation of sample id, sample name, and
        sample barcode bases (expected not observed), delimited by '-'.

        If unmatched is True, the sample name used will be "unmatched".
        """
        sample_name = "unmatched" if unmatched else self.__dict['sample_name']

        if illumina_naming:
            return f"{sample_name}_S{self.__sample_ordinal:d}_L001"
        else:
            sample_barcode_column = sample_barcode_column.lower()
            sample_id			  = self.__dict['sample_id']
            sample_barcode_bases  = self.__dict[sample_barcode_column]
            return f"{sample_id}-{sample_name}-{sample_barcode_bases}"

    def sample_name(self):
        """ Gets the sample name. """
        return self.__dict['sample_name']

    def library_id(self):
        """ Gets the library id, or sample id if library id is missing. """
        if 'library_id' in self.__dict:
            return self.__dict['library_id']
        else:
            return self.__dict['sample_id']
        
    def get(self, key):
        """ Gets the value for the given key. """
        return self.__dict[key]

    @staticmethod
    def samples_from(data, logging=True):
        """
        Reads an Illumina Experiment Manager Sample Sheet or metadata input file and returns
        a list of samples.
        """
        lines = [line.rstrip("\r\n") for line in data.split("\r\n")]
        line_iter = iter(line for line in lines)
        try:
            next(iter(line for line in lines if "[Data]" in line))
            if logging:
                sys.stderr.write("Assuming input metadata file is an Illumina Experiment Manager Sample Sheet.\n")
            while line_iter:
                line = next(line_iter)
                if "[Data]" in line:
                    break
        except StopIteration:
            if logging:
                sys.stderr.write("Assuming input metadata file is simple CSV file.\n")

        samples = []
        header = [line.lower() for line in next(line_iter).split(",")]
        for sample_index, line in enumerate(line_iter):
            sample_data = line.split(",")
            sample_dict = dict(zip(header, sample_data))
            sample	    = Sample(sample_dict, sample_ordinal=sample_index+1)
            samples.append(sample)
        return samples

