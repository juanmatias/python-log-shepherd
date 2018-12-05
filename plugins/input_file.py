#!/usr/bin/env python

# Python Log Shepherd - Input Plugin
# Script to read data sources and send data to consumer (kafka, logstash, etc)
# Author: Juan Matias KungFu de la Camara Beovide <juanmatias@gmail.com>
# Date: 2018-11-5

import logging
import time
import os
import io
import glob
import vendors.ConfigParser as ConfigParser
import pickle

# This is the file reader plugin
# It reads a file from a set of paths
# These paths are set in config/input_file.conf

class file_reader:
  file_positions = {}

  def __init__(self):
    logging.info("Reading config file for input_file module")
    try:
      config_file = os.path.dirname(os.path.realpath(__file__)) + '/../config/input_file.conf'
      self.configParser = ConfigParser.RawConfigParser()
      self.configParser.read(config_file)
      self.MaxBytes = int(self.configParser.get('Input','MaxBytes'))
    except Exception as error:
      raise ValueError('Error reading config file '+config_file+' ('+repr(error)+')')

    logging.info("Open registry file")
    registryFileFullPath = self.configParser.get('Registry','Path')
    try:
      with io.open(registryFileFullPath, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        self.file_positions = pickle.load(f)
    except IOError:
      logging.error('There was an IOError trying to Open regitry file')
      self.file_ack()
      with io.open(registryFileFullPath, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        self.file_positions = pickle.load(f)
    except Exception as error:
      raise ValueError('Error opening registry file '+self.configParser.get('Registry','Path')+' ('+repr(error)+')')

  def file_read(self,data):
    # Actions to take to read data
    logging.info("Reading data from sources")
    file_collection = []
    for f in self.configParser.get('Input','Paths').split(','):
      file_collection.extend(glob.glob(f))
    for f in file_collection:
      logging.info("Reading data from "+f)
      try:
        if not f in self.file_positions:
          self.file_positions[f] = {'offset':0,'inode':-1}
        logging.info("Looking for inode")
        inode=os.stat(f).st_ino
        if self.file_positions[f]['inode'] != inode:
          logging.info('inode has changed, log file was rotated, must read from beginning (  '+str(self.file_positions[f]['inode'])+' vs. '+str(os.stat(f).st_ino)+')')
          self.file_positions[f]['offset'] = 0
        with io.open(f, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as fs:
          if self.file_positions[f]['offset'] == 0 and self.MaxBytes != -1 and self.MaxBytes < os.fstat(
              fs.fileno()).st_size:
            self.file_positions[f]['offset'] = os.fstat(fs.fileno()).st_size - self.MaxBytes
            logging.info("Resetting offset from 0 to {} - {} = {} ".format(os.fstat(fs.fileno()).st_size, self.MaxBytes,self.file_positions[f]['offset']))
          logging.info("Looking for offset "+str(self.file_positions[f]['offset']))
          fs.seek(self.file_positions[f]['offset'])
          localdata = map(lambda x: {'message':x,'source':f}, fs.readlines())
          data.extend(localdata)
          self.file_positions[f]['offset'] = fs.tell()
          self.file_positions[f]['inode'] = inode
      except IOError:
        logging.info('File '+f+' does not exist')
      except Exception as error:
        logging.warning('Error reading source '+f+' ('+repr(error)+')')


  def file_shutdown(self):
    # Actions to take on process shutdown
    return True

  def file_ack(self):
    # Actions to take when sent data ack is received
    logging.info("Pickle file_positions to file")
    registryFileFullPath = self.configParser.get('Registry','Path')
    try:
      with io.open(registryFileFullPath, mode='wb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
        pickle.dump(self.file_positions, f)
    except Exception as error:
      logging.error('There was an error checking the Registry File: ' + registryFileFullPath)
      logging.error(str(error))
      raise ValueError('Error piclking var')
    return True

if __name__ == "__main__":
  quit()
