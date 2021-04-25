#!/usr/bin/python

import os, sys, re, subprocess, tempfile, json, pickle, random, time

#last_analyses = os.path.abspath('/home/minseok/Heap-Doop/luindex-db')


def RunF(pgm, allocs):
  
  f = open("Research.facts",'w')  
  for i, val in enumerate(allocs):
    data = val + '\n'
    f.write(data)
  f.close()
  
  cmd = 'python types_to_facts.py aa Research.facts'
  output = subprocess.check_output(cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)
  
  empty_cache_cmd = 'rm -rf cache/analysis'
  tmp = os.system(empty_cache_cmd)
  if not(tmp == 0):
    print ('Failed to {}/cache'.format(doop_path))
    sys.exit()
  

  cmd = './run -jre1.6 -phantom -heap-abstraction HeapAbstraction.myfacts 3-object-sensitive+2-heap {}'.format(pgm)
  output = subprocess.check_output(cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)
  
 
  #output = subprocess.check_output(cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)

  cast_unproven_query_cmd = 'bloxbatch -db last-analysis -query "Stats:Simple:PotentiallyFailingCast"'
  output = subprocess.check_output(cast_unproven_query_cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)
  cast_unproven_queries = len([cast_unproven_query.strip() for cast_unproven_query in output.splitlines()])

  return cast_unproven_queries
  


def LearnMinimalType(pgm, candidate_types, current_types):
  print 'Initialize'
  current_minimal = current_types 
  print 'Original abstraction size : {}'.format(len(current_minimal))
  current_prec = RunF(pgm, current_minimal)
  print 'Original precision : {}'.format(current_prec)
  while(len(candidate_types) > 0):
    tmp_current_types = current_types
    one_type = candidate_types.pop()
    tmp_current_types.add(one_type)
    print "OneType : {}".format(one_type)
    new_prec = RunF(pgm, tmp_current_types)
    if new_prec < current_prec:
      current_types = tmp_current_types
      print 'We find a worthful type Now : {}'.format(len(current_types))
      f = open(("Learned_Types.facts"),'w')
      for i, val in enumerate(current_types):
        data = val + '\n'
        f.write(data)
      f.close()
    print "Left : {}".format(len(candidate_types))
 
  return current_types 


if __name__ == '__main__':
  pgm = sys.argv[1]
  print ("Run program with ci analysis")
  cmd = './run -jre1.6 -phantom context-insensitive {}'.format(pgm)
  output = subprocess.check_output(cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)
  #types_filename = sys.argv[2]
  #print(pgm)
  print ("Writing facts")


  query = 'bloxbatch -db last-analysis -query ReachableType | sort > facts/ReachableType.facts'
  os.system(query)


  with open("facts/ReachableType.facts", 'r') as f:
    candidate_types = set([t.strip() for t in f.read().splitlines()])
  f.close()
   
  with open("facts/default_alloc_type.facts", 'r') as f:
    current_types = set([t.strip() for t in f.read().splitlines()])
  f.close()
 
  print len(candidate_types)
  print len(current_types)
  print len(candidate_types - current_types)
  

  #allocs_set = set(allocs)
  #minimals_set = set()
  #print 'Original # of allocations : {}'.format(len(allocs_set))
  candidate_types = candidate_types - current_types

  minimal_abstraction_type = LearnMinimalType(pgm, candidate_types, current_types)
  
  f = open(("Learned_Types.facts".format(pgm)),'w')
  for i, val in enumerate(minimal_abstraction_type):
    data = val + '\n'
    f.write(data)
  f.close()
  
  f = open(("Research.facts".format(pgm)),'w')
  for i, val in enumerate(minimal_abstraction_type):
    data = val + '\n'
    f.write(data)
  f.close()
  '''
  print ("Run program with ci analysis 2")
  cmd = './run -jre1.6 -phantom context-insensitive {}'.format(pgm)
  output = subprocess.check_output(cmd + '; exit 0;', stderr=subprocess.STDOUT, shell=True)
  #types_filename = sys.argv[2]
  #print(pgm)
  print ("Writing facts")
  


  query = 'bloxbatch -db last-analysis -query MyReachableHeap | sort > facts/ReachableHeap.facts'
  os.system(query)

  with open("facts/ReachableHeap.facts", 'r') as f:
    candidate_heaps = set([t.strip() for t in f.read().splitlines()])
  f.close()
   
  current_heaps = set()
  
  print len(candidate_heaps)
  print len(current_heaps)

  minimal_abstraction = LearnMinimalHeap(pgm, candidate_heap, current_heap)
  '''



