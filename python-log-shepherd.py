#!/usr/bin/env python3

# Python Log Shepherd
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-5

import logging
import time
import importlib
import signal
import vendors.ConfigParser as ConfigParser
import os

from __version__ import _version
_appname = 'Python Log Shepherd'
_appnametag = 'python-log-shepherd'

class shepherd_importer:
  def pimport(self,plugin, class_name):
    try:
      module = importlib.import_module("."+plugin, "plugins")
      class_ = getattr(module, class_name)
      instance = class_()
      return instance
    except Exception as error:
      raise ValueError('Can not import module '+plugin+' ('+repr(error)+')')
    
class shepherd_reader:
  def __init__(self, plugin):
    assert isinstance(plugin, str), 'Plugin must be str'
    
    if(plugin==''):
      logging.warning('Reader plugin can\'t be empty')
      quit()
    self.plugin = plugin
    logging.info('Trying to load reader plugin: '+self.plugin)
    si = shepherd_importer()
    try:
      self.r = si.pimport("input_"+self.plugin,self.plugin+"_reader")
    except Exception as error:
      logging.error('Got an error calling module: ' + repr(error))
      quit()
    
  
  def read(self, data):
    assert isinstance(data, list), 'Data must be a list'
    logging.info('Reading data')
    try:
      getattr(self.r,self.plugin+"_read")(data)
    except Exception as error:
      logging.error('Got an error reading data: ' + repr(error))
      return False
    return True

  def lower_the_herd(self):
    getattr(self.r,self.plugin+"_shutdown")()
    return True

  def ack(self):
    getattr(self.r,self.plugin+"_ack")()
    return True

  
class shepherd_filter:
  def __init__(self, plugin):
    assert isinstance(plugin, str) or isinstance(plugin, list), 'Plugin must be str or list'
    self.plugins = []
    self.f = []

    if(isinstance(plugin, str) and plugin!=''):
      logging.info('Setting reader plugin name to import: '+plugin)
      self.plugins.append(plugin)
    else:
      self.plugins = plugin
      
    if(len(self.plugins)>0):
      si = shepherd_importer()
      logging.info('Trying to load {} filter plugin/s'.format(len(self.plugins)))
      for pluginname in self.plugins:
        try:
          logging.info('Adding filter {}'.format(pluginname))
          self.f.append(si.pimport("filter_"+pluginname,pluginname+"_filter"))
        except Exception as error:
          logging.error('Got an error calling module: ' + repr(error))
          quit()
    else:
      logging.info('No need to load filters.')
      
  def filter(self,data):
    assert isinstance(data, list), 'Data must be a list'
    logging.info('Filtering data')
    if len(self.plugins) == 0:
      logging.info('No filtering needed')
      return True
    for idx,current_filter in enumerate(self.plugins):
      logging.info('Applying filter: {}'.format(current_filter))
      getattr(self.f[idx],current_filter+"_filter")(data)

    return True
    
  def lower_the_herd(self):
    # ~ if len(self.plugins) > 0:
      # ~ getattr(self.f,self.plugins+"_shutdown")()
    return True
  
class shepherd_writer:
  def __init__(self, plugin):
    assert isinstance(plugin, str), 'Plugin must be str'
    if(plugin==''):
      logging.warning('Writer plugin can\'t be empty')
      quit()
    self.plugin = plugin
    logging.info('Trying to load writer plugin: '+self.plugin)
    si = shepherd_importer()
    try:
      self.w = si.pimport('output_'+self.plugin,self.plugin+"_writer")
    except Exception as error:
      logging.error('Got an error calling module: ' + repr(error))
      quit()

  def write(self, data):
    assert isinstance(data, list), 'Data must be a list'

    logging.info('writting data:')
    try:
      local_data = []
      for d in data:
        tags = [_appnametag]
        if '@tags' in d:
          tags.extend(d['@tags'])
        d['@tags'] = tags
        d['@timestamp'] =  time.time()
        local_data.append(d)
      getattr(self.w,self.plugin+"_write")(local_data)
    except Exception as error:
      logging.error('Got an error calling module: ' + repr(error))
      return False
    logging.info('flushing buffer')
    del data[:]
    return True

  def lower_the_herd(self):
    getattr(self.w,self.plugin+"_shutdown")()
    return True

class python_shepherd:
  interval_default = 5
  shepherd_buffer = []
  
  def __init__(self):
    # Set log level
    logging.basicConfig(format='%(asctime)s %(levelname)s ( %(module)s ):%(message)s',level=logging.DEBUG)
    signal.signal(signal.SIGINT, self.lower_the_herd)
    logging.info('{} version: {}'.format(_appname,_version))
    logging.info('Reading config file for main process')
    self.configParser = ConfigParser.RawConfigParser()   
    config_file = os.path.dirname(os.path.realpath(__file__)) + '/config/python-log-shepherd.conf'
    self.configParser.read(config_file)
    self.reader_plugin = self.configParser.get('Plugins','Reader')
    self.filter_plugin = self.configParser.get('Plugins','Filter').split(',')
    self.writer_plugin = self.configParser.get('Plugins','Writer')
    if(isinstance(int(self.configParser.get('Config','Interval')),int)):
      logging.info('Changing interval to '+self.configParser.get('Config','Interval'))
      self.interval_default = int(self.configParser.get('Config','Interval'))
    
  def lower_the_herd(self,sig, frame):
    if(sig != None):
      logging.info('SIG {} received'.format(sig))
    logging.info('Shutting down child processes')
    try:
      self.sr.lower_the_herd()
      self.sf.lower_the_herd()
      self.sw.lower_the_herd()
    except Exception as error:
      logging.error('Got an error shutting proccesses down: ' + repr(error))
    logging.info('Shutting down main process')
    quit()
    
  def graze(self):
    # Start work
    logging.info('Initializing objects')
    try:
      self.sr = shepherd_reader(self.reader_plugin)
      self.sf = shepherd_filter(self.filter_plugin)
      self.sw = shepherd_writer(self.writer_plugin)
    except Exception as error:
      logging.error('Got an error creating plugins: ' + repr(error))
      quit()

    logging.info('Initializing job')
    while True:
      logging.info('Calling reader')
      if(self.sr.read(self.shepherd_buffer)):
        if(len(self.shepherd_buffer)>0):
          logging.info('Calling filter')
          if(self.sf.filter(self.shepherd_buffer)):
            logging.info('Calling writer')
            if(self.sw.write(self.shepherd_buffer)):
              logging.info('Logs processed')
              if(self.sr.ack()):
                logging.info('Ack sent to reader')
              else:
                logging.error('Ack error')
                quit()
            else:
              logging.error('Writer error')
              quit()
          else:
            logging.error('Filter error')
            quit()
        else:
          logging.info('No data to process')
      else:
        logging.error('Reader error')
        quit()
      
      if(self.interval_default != -1):
        time.sleep(self.interval_default)
      else:
        self.lower_the_herd(None,None)
    
  
if __name__ == "__main__":
  ps = python_shepherd()
  ps.graze()


