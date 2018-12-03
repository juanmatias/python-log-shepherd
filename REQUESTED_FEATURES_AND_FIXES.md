# Python Log Shepherd

A simple Python logs shipper.

![shepherd](images/shepherd.png  "shepherd")

## Requested Features

| \# | Name | Description | Added in commit | Date |
| :----------- | ----------: | :---------------: | | | 
|  1  | Filename Wildcard in input_file | Add the ability to handle wildcards for files definitions in input_file | 5770edca3cd15f297600462cf3e1674c9181ca00 | develop 1.1.0 | 
|  2  | Add filters to core | Add the ability to call multiple filters after data input and before data output. | 776f0fb8465bcd7b26db9a6f07515f3306eb07dd | develop 1.1.0 | 
|  3  | Add server data to event | Add a few data from server such IP and name  | 37833cf1ea9d4803a79f5b90b93537e74f8a63c8 | develop 1.1.0 | 
|  4  | Add custom tags to event | Add a plugin that allows to add custom tags to events  | ed8ece129c8a89d518009821994a9a96f70224c5 | develop 1.1.0 | 
|  5  | Improve the cli | Add the ability to receive cli parameters to set configuration values | | | 
|  6  | Logs rotation | Allow logs rotation and old logs deletion | | | 
|  7  | Improve documentation | Improve all in-code documentation according to standars | | | 


## Requested Fixes

| \# | Name | Description | Added in commit | Date |
| :----------- | ----------: | :---------------: | | | 
|  1  | regexsimpleproc overwrites target field | If two or more regexps set the same target field (e.g. extracted) the field is overwritten, it should add the no existent fields under target field | 40aebd0ed058d703b1f99c73fb4677aefb4724a3 | develop 1.1.0 | 
|  2  | Memory limit to read files | Add a limit whe reading a new file from beginning so we do not use all the available memory | 237910c252ed87e41800c6b0c34de5466e105e8d | develop 1.1.0 | 
