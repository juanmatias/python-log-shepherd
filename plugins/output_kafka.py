#!/usr/bin/env python

# Python Log Shepherd - Output Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-5

import logging
import json
import vendors.ConfigParser as ConfigParser
import os
from kafka import KafkaProducer
import time

# This is the writer to kafka plugin
# Must have a class called <plugin_name>_writer
# This class must have the following methods:
#  - <plugin_name>_write
#  - <plugin_name>_shutdown

class kafka_writer:
  producer = None
  
  def __init__(self):
    logging.info("Reading config file for output_kafka module")
    try:
      config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config/output_kafka.conf'
      self.configParser = ConfigParser.RawConfigParser()
      self.configParser.read(config_file)
    except Exception as error:
      raise ValueError('Error reading config file '+config_file+' ('+repr(error)+')')

    try:
      self.topic = self.configParser.get('Config','Topic')
      self.t = self.configParser.get('Config','t')
      self.e = self.configParser.get('Config','e')
      self.servers = self.configParser.get('Config','Servers')
      self.reconnection_max = self.configParser.get('Config','Reconnection_max')
    except Exception as error:
      raise ValueError('Error reading values from config file ('+repr(error)+')')

    self._kafka_connect()
    
  def _kafka_connect(self):
    try:
      logging.info("Creating producer...")
      self.producer = KafkaProducer(bootstrap_servers=self.servers)
    except Exception as error:
      raise ValueError('Error connecting to kafka ('+repr(error)+')')

  def kafka_write(self,data):
    # Actions to take to write data
    if(self.producer == None):
      self._kafka_connect()

    # SEND DATA TO FRANZ
    data_sent = False
    try:
      logging.info("Sending message...")
      data_str_to_send = ''
      counter = 0
      for d in data:
        sent = self.producer.send(self.topic, json.dumps(d, indent=4).encode('utf-8'))
        result = sent.get(timeout=60)
        counter += 1
        if float(self.t) > 0 and int(self.e) <= counter:
          time.sleep(float(self.t))
          counter = 0
    except Exception as error:
      self.producer = None
      logging.warning('Error sending data to kafka ('+repr(error)+')')
      return False

    return True
  
  def kafka_shutdown(self):
    # Actions to take on process shutdown
    return True


if __name__ == "__main__":
  quit()


