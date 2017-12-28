import unittest

from basespace_commons.sample import Sample

class TestSample(unittest.TestCase):

    def test_init_require_sample_name(self):
        with self.assertRaises(KeyError):
            Sample({'sample_id' : 'id'}, 1)
        with self.assertRaises(AssertionError):
            sample = Sample({'sample_name' : None, 'sample_id' : 'id'}, 1)

    def test_init_require_sample_id(self):
        with self.assertRaises(KeyError):
            Sample({'sample_name' : 'name'}, 1)
        with self.assertRaises(AssertionError):
            sample = Sample({'sample_name' : 'name', 'sample_id' : None}, 1)

    def test_init_require_sample_ordinal_geq_one(self):
        with self.assertRaises(AssertionError):
            Sample({'sample_name' : 'name', 'sample_id' : 'id'}, 0)

    def test_init_ok(self):
        sample = Sample({'sample_name' : 'name', 'sample_id' : 'id'}, 1)
        self.assertEqual(sample.sample_name(), 'name')
        self.assertEqual(sample.sample_id(), 'id')
        self.assertEqual(sample.sample_ordinal(), 1)

    def test_bam_matched(self):
        matchedSample = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA'}, 1) 
        self.assertEqual(matchedSample.bam(dir='dir', unmatched=False, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-matched-GATTACA.bam')
        self.assertEqual(matchedSample.bam(dir='dir', unmatched=False, illumina_naming=True, sample_barcode_column=None), 'dir/matched_S1_L001.bam')

    def test_bam_unmatched(self):
        unmatchedSample = Sample({'sample_name' : 'unmatched', 'sample_id' : 'id', 'sample_barcode' : 'NNNNNNN'}, 2) 
        self.assertEqual(unmatchedSample.bam(dir='dir', unmatched=True, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-unmatched-NNNNNNN.bam')
        self.assertEqual(unmatchedSample.bam(dir='dir', unmatched=True, illumina_naming=True, sample_barcode_column='sample_barcode'), 'dir/unmatched_S2_L001.bam')

    def test_fq_matched(self):
        matchedSample = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA'}, 1) 
        self.assertEqual(matchedSample.fq(dir='dir', end=1, unmatched=False, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-matched-GATTACA_R1_001.fastq.gz')
        self.assertEqual(matchedSample.fq(dir='dir', end=1, unmatched=False, illumina_naming=True, sample_barcode_column=None), 'dir/matched_S1_L001_R1_001.fastq.gz')
        self.assertEqual(matchedSample.fq(dir='dir', end=2, unmatched=False, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-matched-GATTACA_R2_001.fastq.gz')
        self.assertEqual(matchedSample.fq(dir='dir', end=2, unmatched=False, illumina_naming=True, sample_barcode_column=None), 'dir/matched_S1_L001_R2_001.fastq.gz')

    def test_fq_unmatched(self):
        unmatchedSample = Sample({'sample_name' : 'unmatched', 'sample_id' : 'id', 'sample_barcode' : 'NNNNNNN'}, 2) 
        self.assertEqual(unmatchedSample.fq(dir='dir', end=1, unmatched=True, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-unmatched-NNNNNNN_R1_001.fastq.gz')
        self.assertEqual(unmatchedSample.fq(dir='dir', end=1, unmatched=True, illumina_naming=True, sample_barcode_column='sample_barcode'), 'dir/unmatched_S2_L001_R1_001.fastq.gz')
        self.assertEqual(unmatchedSample.fq(dir='dir', end=2, unmatched=True, illumina_naming=False, sample_barcode_column='sample_barcode'), 'dir/id-unmatched-NNNNNNN_R2_001.fastq.gz')
        self.assertEqual(unmatchedSample.fq(dir='dir', end=2, unmatched=True, illumina_naming=True, sample_barcode_column='sample_barcode'), 'dir/unmatched_S2_L001_R2_001.fastq.gz')
    
    def test_prefix_matched(self):
        matchedSample = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA'}, 1) 
        self.assertEqual(matchedSample.prefix(unmatched=False, illumina_naming=False, sample_barcode_column='sample_barcode'), 'id-matched-GATTACA')
        self.assertEqual(matchedSample.prefix(unmatched=False, illumina_naming=True, sample_barcode_column=None), 'matched_S1_L001')
        with self.assertRaises(AssertionError):
            matchedSample.prefix(unmatched=False, illumina_naming=False, sample_barcode_column=None)

    def test_prefix_unmatched(self):
        unmatchedSample = Sample({'sample_name' : 'unmatched', 'sample_id' : 'id', 'sample_barcode' : 'NNNNNNN'}, 2) 
        self.assertEqual(unmatchedSample.prefix(unmatched=True, illumina_naming=False, sample_barcode_column='sample_barcode'), 'id-unmatched-NNNNNNN')
        self.assertEqual(unmatchedSample.prefix(unmatched=True, illumina_naming=True, sample_barcode_column='sample_barcode'), 'unmatched_S2_L001')
        with self.assertRaises(AssertionError):
            unmatchedSample.prefix(unmatched=True, illumina_naming=False, sample_barcode_column=None)
    
    def test_library_id(self):
        libraryId = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA', 'library_id' : 'lid'}, 1) 
        self.assertEqual(libraryId.library_id(), 'lid')

        noLibraryId = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA'}, 1) 
        self.assertEqual(noLibraryId.library_id(), 'id')

    def test_get(self):
        sample = Sample({'sample_name' : 'matched', 'sample_id' : 'id', 'sample_barcode' : 'GATTACA', 'fun_key' : 'fun_value'}, 1) 
        self.assertEqual(sample.get('fun_key'), 'fun_value')
        with self.assertRaises(KeyError):
            self.assertEqual(sample.get('boring_key'))

    def test_samples_from_sample_sheet(self):
        sample_sheet = """
[Header],,,,,,,,,,,
IEMFileVersion,4,,,,,,,,,,
Investigator Name,Joe,,,,,,,,,,
Experiment Name,EXPID,,,,,,,,,,
Date,1/1/00,,,,,,,,,,
Workflow,GenerateFASTQ,,,,,,,,,,
Application,FASTQ Only,,,,,,,,,,
Assay,Assay Name,,,,,,,,,,
Description,The Description,,,,,,,,,,
Chemistry,Amplicon,,,,,,,,,,
,,,,,,,,,,,
[Reads],,,,,,,,,,,
151,,,,,,,,,,,
151,,,,,,,,,,,
,,,,,,,,,,,
[Settings],,,,,,,,,,,
ReverseComplement,0,,,,,,,,,,
Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,,,
AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,,,
,,,,,,,,,,,
[Data],,,,,,,,,,,
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Sample_Barcode,R2_Barcode_Bases,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description
1,N1,,,AAAAAAAA,,,,,,,
2,N2,,,CCCCCCCC,,,,,,,
3,N3,,,GGGGGGGG,,,,,,,
4,N4,,,TTTTTTTT,,,,,,,
5,N5,,,NNNNNNNN,,,,,,,
        """
        samples = Sample.samples_from(data=sample_sheet, logging=False)
        self.assertListEqual([s.sample_id() for s in samples], ["1", "2", "3", "4", "5"])
        self.assertListEqual([s.sample_name() for s in samples], ["N1", "N2", "N3", "N4", "N5"])
        self.assertListEqual([s.get('sample_barcode') for s in samples], ["A"*8, "C"*8, "G"*8, "T"*8, "N"*8])

    def test_samples_from_metadata(self):
        sample_sheet = """
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Sample_Barcode,R2_Barcode_Bases,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description
1,N1,,,AAAAAAAA,,,,,,,
2,N2,,,CCCCCCCC,,,,,,,
3,N3,,,GGGGGGGG,,,,,,,
4,N4,,,TTTTTTTT,,,,,,,
5,N5,,,NNNNNNNN,,,,,,,
        """
        samples = Sample.samples_from(data=sample_sheet, logging=False)
        self.assertListEqual([s.sample_id() for s in samples], ["1", "2", "3", "4", "5"])
        self.assertListEqual([s.sample_name() for s in samples], ["N1", "N2", "N3", "N4", "N5"])
        self.assertListEqual([s.get('sample_barcode') for s in samples], ["A"*8, "C"*8, "G"*8, "T"*8, "N"*8])

