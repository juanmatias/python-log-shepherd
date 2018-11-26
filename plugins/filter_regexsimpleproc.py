#!/usr/bin/env python

# Python Log Shepherd - Filter Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-26

import logging
import re
import vendors.ConfigParser as ConfigParser
import os

# This is the filter plugin
# Must have a class called <plugin_name>_filter
# This class must have the following methods:
#  - <plugin_name>_filter
#  - <plugin_name>_shutdown
#  - <plugin_name>_ack

class regexsimpleproc_filter:

  def __init__(self):
    logging.info("Reading config file for regexsimpleproc module")
    try:
      config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config/filter_regexsimpleproc.conf'
      self.configParser = ConfigParser.ConfigParser()
      self.configParser.read(config_file)
    except Exception as error:
      raise ValueError('Error reading config file ' + config_file + ' (' + repr(error) + ')')

  def regexsimpleproc_filter(self,data):
    # Actions to take to filter data
    logging.info('Applying regexsimpleproc filter')

    # Data is a dict object
    # Meesage sample line: <Nov 26, 2018 5:52:08 AM ART> <Error> <oracle.osb.transports.mq.mqtransport> <OSB-381916> <Error occurred when connecting to MQ: Queue TN.PRES.OBTENER.COMPPREST.NOL.RES does not exist on Queue Manager TNQMDESA>
    # all following lines belong to the same event

    logging.info('Applying filters {}'.format(self.configParser.sections()))
    for idx, item in enumerate(data):
      for section in self.configParser.sections():

        current_source = self.configParser.get(section, 'Current_source')
        current_target_root = self.configParser.get(section, 'Current_target_root')
        current_regex = re.compile(self.configParser.get(section, 'Current_regex'),re.S)
        current_fields = self.configParser.get(section, 'Current_fields').split(',')


        message = item[current_source]
        if current_target_root != '':
          item[current_target_root] = {}
        current_match = current_regex.match(message)
        if current_match:
          for cmidx,cm in enumerate(current_match.groups()):
            if current_target_root != '':
              item[current_target_root][current_fields[cmidx]] = cm
            else:
              item[current_fields[cmidx]] = cm

      data[idx] = item
    
  def regexsimpleproc_shutdown(self):
    # Actions to take on process shutdown
    return True
  
  def regexsimpleproc_ack(self):
    # Actions to take when sent data ack is received
    return True
    
if __name__ == "__main__":
  quit()


