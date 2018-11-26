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

class multiline_filter:

  def __init__(self):
    logging.info("Reading config file for multiline module")
    try:
      config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config/filter_multiline.conf'
      self.configParser = ConfigParser.ConfigParser()
      self.configParser.read(config_file)
    except Exception as error:
      raise ValueError('Error reading config file ' + config_file + ' (' + repr(error) + ')')

  def multiline_filter(self, data):
    # Actions to take to filter data
    logging.info('Applying multiline filter')

    # Data is a dict object
    # Meesage sample line: <Nov 26, 2018 5:52:08 AM ART> <Error> <oracle.osb.transports.mq.mqtransport> <OSB-381916> <Error occurred when connecting to MQ: Queue TN.PRES.OBTENER.COMPPREST.NOL.RES does not exist on Queue Manager TNQMDESA>
    # all following lines belong to the same event

    data_aux = []
    message_aux = ''
    first_item_in_line = {}
    line_source = self.configParser.get('Multiline', 'Line_source')
    line_start = re.compile(self.configParser.get('Multiline', 'Line_start'))
    line_end = re.compile(self.configParser.get('Multiline', 'Line_end'), re.M)

    for item in data:
      line_start_match = line_start.search(item[line_source])
      line_end_match = line_end.search(item[line_source].rstrip())

      # If beginning-of-line matches then start record the item
      if line_start_match:
        logging.debug('Line Start Matched')
        message_aux = item[line_source]
        first_item_in_line = item

      if not line_start_match and message_aux == '':
        logging.debug('Orphan Line Matched')
        data_aux.append(item)

      # If not start and I'm not building an event then send line as is
      if not line_start_match and message_aux != '':
        message_aux += item[line_source]

      # If end-of-line matches then save item and reset values
      if line_end_match and message_aux != '':
        logging.debug('Line End Matched')
        first_item_in_line['message'] = message_aux
        data_aux.append(first_item_in_line)
        message_aux = ''
        first_item_in_line = {}

    if len(data_aux) > 0:
      logging.info('Merging data')
      del data[:]
      data.extend(data_aux)
    else:
      logging.info('No data to merge')

  def multiline_shutdown(self):
    # Actions to take on process shutdown
    return True

  def multiline_ack(self):
    # Actions to take when sent data ack is received
    return True


if __name__ == "__main__":
  quit()


