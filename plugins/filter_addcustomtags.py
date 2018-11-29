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

class addcustomtags_filter:

  def __init__(self):
    logging.info("Reading config file for addcustomtags module")
    try:
      config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config/filter_addcustomtags.conf'
      self.configParser = ConfigParser.ConfigParser()
      self.configParser.read(config_file)
    except Exception as error:
      raise ValueError('Error reading config file ' + config_file + ' (' + repr(error) + ')')

  def addcustomtags_filter(self, data):
    # Actions to take to filter data
    logging.info('Applying addcustomtags filter')

    # Data is a dict object

    logging.info('Applying filters {}'.format(self.configParser.sections()))

    for idx, item in enumerate(data):

      for section in self.configParser.sections():

        custom_tags = self.configParser.get(section, 'CustomTags').split(',')
        custom_regex_source = self.configParser.get(section, 'CustomRegexSource')
        if self.configParser.get(section, 'CustomRegex') != '':
          custom_regex = re.compile(self.configParser.get(section, 'CustomRegex'), re.S)
        else:
          custom_regex = ''

        current_match = (custom_regex=='' or custom_regex.match(item[custom_regex_source]))
        if current_match:
          if not '@tags' in item:
            logging.debug('Adding key @tags to item: {}: '.format(item))
            item['@tags'] = []
          logging.debug('Extending @tags')
          item['@tags'].extend(custom_tags)

      data[idx] = item

  def addcustomtags_shutdown(self):
    # Actions to take on process shutdown
    return True

  def addcustomtags_ack(self):
    # Actions to take when sent data ack is received
    return True


if __name__ == "__main__":
  quit()


