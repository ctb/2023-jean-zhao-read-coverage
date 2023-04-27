# 2023-jean-zhao-read-coverage

This script requires `pysam`, which can be installed via conda.

The script runs like so:
```
./calc-coverage-diff-sam-bam.py ERR257715.x.GCF_003352045.1.bam ERR257715.x.GCF_003352045.1.diff.reads.x.genome.bam -o xxx.csv
```
and it will output a CSV (`xxx.csv`) for each read in the second BAM,
indicating the coverage of its location in the first BAM.

For example, the first BAM might contain _all_ reads mapped to a
genome, and the second BAM might contain a subset of those reads
whose coverage in the first BAM you're interested in.

Both BAMs should be mapped to the same reference and both BAMs should
be indexed and sorted (`samtools sort`, `samtools index`).
