import unittest

from basespace_commons import sample

class TestSample(unittest.TestCase):
    # Tests to write

    # init a sample, require 'sample_name'
    # init a sample, require 'sample_id'
    # init a sample, sample ordinal > 0

    # bam() with a matched/unmatched sample
    # bam() with illumina_naming True/False
    # bam() with illumina_naming False but no sample_barcode_column
    
    # fq() with end 1 or 2
    # fq() with end out of range
    # fq() with a matched/unmatched sample
    # fq() with illumina_naming True/False
    # fq() with illumina_naming False but no sample_barcode_column
    
    # prefix() with a matched/unmatched sample
    # prefix() with illumina_naming True/False
    # prefix() with illumina_naming False but no sample_barcode_column

    # get_sample_name()

    # library_id with library id present/missing

    # get arbitrary key 

    # samples_from() SampleSheet.csv
    # samples_from() metadata.csv

    pass
