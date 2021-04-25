#!/usr/bin/python

from collections import defaultdict
import os, sys, re, subprocess, tempfile, json, pickle, random, time

if __name__ == '__main__':
  types_filename = sys.argv[1]
  with open(types_filename, 'r') as f:
    types = [t.strip() for t in f.read().splitlines()]

  cnt = 0
  for i, val in enumerate(types):
    index = 0 
    for j, char in enumerate(val):
      if (char == '<') and (val[j+1] == '-'):
        index = val[j-2] 
    
    cmd = 'Feature{}(?heap{}),'.format(cnt,index) 
    cnt = cnt+1
    print cmd+val



   

