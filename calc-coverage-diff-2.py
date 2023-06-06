#! /usr/bin/env python
"""
"""
import sys
import argparse
import pysam
import csv


def main():
    p = argparse.ArgumentParser()
    p.add_argument('depth_file')
    p.add_argument('query_reads')
    p.add_argument('-o', '--output', help='coverage CSV',
                   required=True)
    args = p.parse_args()

    coverages = {}
    with open(args.depth_file, 'r', newline='') as fp:
        r = csv.reader(fp, delimiter='\t')
        for row in r:
            # unpack row
            contig, pos, depth = row

            # convert to int
            pos, depth = int(pos), int(depth)

            # find depth per contig
            d2 = coverages.get(contig, {})

            # check that it's not being overwritten - basic consistency check
            assert pos not in d2

            # write!
            d2[pos] = depth
            coverages[contig] = d2

    query_bam = pysam.AlignmentFile(args.query_reads, "rb")

    outfp = open(args.output, 'w', newline='')
    w = csv.writer(outfp)
    w.writerow(['read_name','mapping_cov'])

    # iterate over query reads
    fup = query_bam.fetch()
    for n, read in enumerate(fup):
        if n % 100 == 0:
            print('...', n)

        chr = read.reference_name
        start = read.reference_start
        end = read.reference_end
        assert start < end

        # for each position in query read, get coverage
        sum_cov = []
        for pos in range(start, end + 1):
            d2 = coverages.get(chr)
            depth = d2.get(pos, 0)
            sum_cov.append(depth)

        w.writerow([read.qname, f"{sum(sum_cov) / len(sum_cov):.2f}"])

    outfp.close()


if __name__ == '__main__':
    main()
