#!/bin/bash
ip=$(hostname | cut -d - -f 2,3,4,5 | sed 's/-/./g')
name=$ip
name+=".slave"
echo $ip >> $name