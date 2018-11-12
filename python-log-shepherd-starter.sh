#!/bin/bash

# Path to file ending with slash
PATH_TO_PROGRAM="/path/to/your/files/"

# File name as it can be found into processes list
PROGRAM_NAME="python-log-shepherd.py"

# Just in case we have an empty name
if [ "$PROGRAM_NAME" = "" ];
then
        echo "No programname spicifed"
        return 0
fi

# Here is the "potato" (argentinian slang)
if [[ `egrep -f $PROGRAM_NAME` ]];
then
        echo "Program $PROGRAM_NAME already running"
else
        echo "Starting the program: $PROGRAM_NAME"
        nohup sh -c "python3 $PATH_TO_PROGRAM$PROGRAM_NAME >> $PATH_TO_PROGRAM$PROGRAM_NAME.log 2>&1" &
fi

