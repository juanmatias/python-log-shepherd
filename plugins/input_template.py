#!/usr/bin/env python

# Python Log Shepherd - Input Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-5

import logging

# This is the reader plugin
# Must have a class called <plugin_name>_reader
# This class must have the following methods:
#  - <plugin_name>_read
#  - <plugin_name>_shutdown
#  - <plugin_name>_ack

class template-name_reader:
  def template-name_read(self,data):
    # Actions to take to read data
    data.append('sample data')
  
  def template-name_shutdown(self):
    # Actions to take on process shutdown
    return True
  
  def template-name_ack(self):
    # Actions to take when sent data ack is received
    return True
    
if __name__ == "__main__":
  quit()


