# Python Log Shepherd

A simple Python logs shipper.

![shepherd](images/shepherd.png  "shepherd")

## Requested Features

| \# | Name | Description | Added in commit | Date |
| :----------- | ----------: | :---------------: | | | 
|  1  | Filename Wildcard in input_file | Add the ability to handle wildcards for files definitions in input_file | | | 
|  2  | Add filters to core | Add the ability to call multiple filters after data input and before data output. | 776f0fb8465bcd7b26db9a6f07515f3306eb07dd | develop 1.1.0 | 
|  3  | Add server data to event | Add a few data from server such IP and name  | 37833cf1ea9d4803a79f5b90b93537e74f8a63c8 | develop 1.1.0 | 
|  4  | Add custom tags to event | Add a plugin that allows to add custom tags to events  | ed8ece129c8a89d518009821994a9a96f70224c5 | develop 1.1.0 | 
|  5  | Improve the cli | Add the ability to receive cli parameters to set configuration values | | | 


## Requested Fixes

| \# | Name | Description | Added in commit | Date |
| :----------- | ----------: | :---------------: | | | 
|  1  | regexsimpleproc overwrites target field | If two or more regexps set the same target field (e.g. extracted) the field is overwritten, it should add the no existent fields under target field | 40aebd0ed058d703b1f99c73fb4677aefb4724a3 | develop 1.1.0 | 
