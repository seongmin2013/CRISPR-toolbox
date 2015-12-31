#!/usr/bin/env python
import os
import sys

max_freq = 3

filename_sam = sys.argv[1]
filename_out = filename_sam.replace('.sam_hit','')+'.r_freq'

r_list = dict()
f_sam = open(filename_sam,'r')
for line in f_sam:
    if( line.startswith('@') ):
        continue
    tokens = line.strip().split("\t")
    if( len(tokens) < 4 ):
        continue
    r_id = tokens[0]
    if( not r_list.has_key(r_id) ):
        r_list[r_id] = {'total':0, 'perfect':0, 'targets':[]}

    r_list[r_id]['total'] += 1
    if( 'NM:i:0' in tokens ):
        r_list[r_id]['perfect'] += 1

    if( r_list[r_id]['perfect'] <= max_freq ):
        r_list[r_id]['targets'].append('%s|%s'%(tokens[2],tokens[3]))
f_sam.close()

for r_id in sorted(r_list.keys()):
    if( r_list[r_id]['total'] > max_freq ):
        continue
    print "%s\t%d\t%d\t%s"%(r_id, r_list[r_id]['total'], r_list[r_id]['perfect'], ','.join(r_list[r_id]['targets']))
#f_out = open(filename_out,'w')
#f_out.write('#TargetID\tCount\tMinPos\tMaxPos\tPerfectCount\tPerfectMinPos\tPerfectMaxPos\n')
#for t_id in sorted(t_map.keys()):
#    tmp_map = t_map[t_id]
#    f_out.write('%s\t%d\t%d\t%d\t%d\t%d\t%d\n'%(t_id,tmp_map['count'],tmp_map['min_pos'],tmp_map['max_pos'],tmp_map['perfect_count'],tmp_map['perfect_min_pos'],tmp_map['perfect_max_pos']))
#f_out.close()
