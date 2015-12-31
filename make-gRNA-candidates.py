#!/usr/bin/env python
import os
import sys
import gzip

filename_gDNA = '/work/xenopus.genome/XENLA_JGIv91/XENLA_JGIv91_dna_final.fa.gz'
filename_gff = '/work/xenopus.annot/XENLA_JGIv18/XENLA_JGIv18pV2_cds_final.XENLA_JGIv91_dna_final.gmap_gff'

len_gRNA = 23
len_flank = 45

seq_h = ''
seq_list = dict()
f_fa = open(filename_gDNA,'r')
if( filename_gDNA.endswith('.gz') ):
    f_fa = gzip.open(filename_gDNA, 'rb')
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()

exons = dict()
f_gff = open(filename_gff,'r')
for line in f_gff:
    if( line.startswith('#') ):
        continue
    tokens = line.strip().split("\t")
    tmp_type = tokens[2]
    if( tmp_type == 'exon' ):
        tmp_id = tokens[8].split(';')[0].replace('ID=','')
        tmp_chr = tokens[0]
        if( not exons.has_key(tmp_chr) ):
            exons[tmp_chr] = dict()
        exons[tmp_chr][tmp_id] = {'start':int(tokens[3]), 'end':int(tokens[4]), 'strand':tokens[6]}
f_gff.close()

## Rules for gRNA
## %GC > 40 and %GC < 80
## Ends with GG
## No 'N's

def count_GC(tmp_seq):
    return (tmp_seq.count('G') + tmp_seq.count('C'))*100.0/len(tmp_seq)

rc_tbl = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
def revcomp(tmp_seq):
    rv = []
    for tmp_n in tmp_seq[::-1]:
        rv.append(rc_tbl[tmp_n])
    return ''.join(rv)

for tmp_chr in exons.keys():
    tmp_seq = ''.join(seq_list[tmp_chr])
    len_seq = len(tmp_seq)
    if( len_seq < 100 ):
        continue

    for tmp_id in exons[tmp_chr].keys():
        tmp_init = exons[tmp_chr][tmp_id]['start'] - len_flank
        if( tmp_init < 0 ):
            tmp_init = 1
        tmp_end = exons[tmp_chr][tmp_id]['end'] + len_flank
        if( tmp_end > len_seq ):
            tmp_end = len_seq
        for tmp_pos in range(tmp_init, tmp_end):
            tmp_gRNA = tmp_seq[tmp_pos-1:tmp_pos+len_gRNA-1].upper()
            if( tmp_gRNA.find('N') >= 0 ):
                continue
            if( len(tmp_gRNA) != len_gRNA ):
                continue
            tmp_GC = count_GC(tmp_gRNA)
            if( tmp_GC < 40 or tmp_GC > 80 ):
                continue
            if( tmp_gRNA.endswith('GG') ):
                print ">%s|%s|%d|+\n%s"%(tmp_id,tmp_chr,tmp_pos,tmp_gRNA)
            elif( tmp_gRNA.startswith('CC') ):
                print ">%s|%s|%d|-\n%s"%(tmp_id,tmp_chr,tmp_pos,revcomp(tmp_gRNA))
