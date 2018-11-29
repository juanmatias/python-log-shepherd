#!/usr/bin/env python

# Python Log Shepherd - Filter Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-26

import logging

# This is the filter plugin
# Must have a class called <plugin_name>_filter
# This class must have the following methods:
#  - <plugin_name>_filter
#  - <plugin_name>_shutdown
#  - <plugin_name>_ack

class template-name_filter:
  def template-name_filter(self,data):
    # Actions to take to filter data
    for idx, item in enumerate(data):
      # Do what you need here
      item = " modified item " + item
      data[idx] = item
    
    # Other way is using map and lambda
    # data = list(map(lambda x: " modified item " + x, data))
  
  def template-name_shutdown(self):
    # Actions to take on process shutdown
    return True
  
  def template-name_ack(self):
    # Actions to take when sent data ack is received
    return True
    
if __name__ == "__main__":
  quit()


