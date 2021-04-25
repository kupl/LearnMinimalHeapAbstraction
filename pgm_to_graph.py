#!/usr/bin/env python
import os, sys


query = 'bloxbatch -db last-analysis -query ReachableHeap | sort > Nodes.facts'
os.system(query)

query = 'bloxbatch -db last-analysis -query ReachableType | sort > ReachableType.facts'
os.system(query)

