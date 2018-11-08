#!/usr/bin/env python

# Python Log Shepherd - Output Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-5

import logging
import json

# This is the writer to stdout plugin
# Must have a class called <plugin_name>_writer
# This class must have the following methods:
#  - <plugin_name>_write
#  - <plugin_name>_shutdown

class stdout_writer:
  def stdout_write(self,data):
    # Actions to take to write data
    print("{}".format(json.dumps(data, indent=4)))
    return True
  
  def stdout_shutdown(self):
    # Actions to take on process shutdown
    return True
  
if __name__ == "__main__":
  quit()


