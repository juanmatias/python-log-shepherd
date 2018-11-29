#!/usr/bin/env python

# Python Log Shepherd - Filter Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-26

import logging
import platform
import socket

# This is the filter plugin
# Must have a class called <plugin_name>_filter
# This class must have the following methods:
#  - <plugin_name>_filter
#  - <plugin_name>_shutdown
#  - <plugin_name>_ack

class addserverdata_filter:

  def addserverdata_filter(self, data):

    logging.info('Applying addserverdata filter')
    # Actions to take to filter data
    try:
      host_name = socket.gethostname()
      host_ip = socket.gethostbyname(host_name)
    except:
      host_name = 'unknown'
      host_ip = 'unknown'

    hostdata = {
      'platform': platform.platform(),
      'uname': platform.uname(),
      'python_version': platform.python_version_tuple(),
      'libc_ver': platform.libc_ver(),
      'host_name': host_name,
      'host_ip': host_ip
    }
    for idx, item in enumerate(data):
      # Do what you need here
      item['@hostdata'] = hostdata
      data[idx] = item


  def addserverdata_shutdown(self):
    # Actions to take on process shutdown
    return True


  def addserverdata_ack(self):
    # Actions to take when sent data ack is received
    return True

if __name__ == "__main__":
  quit()


