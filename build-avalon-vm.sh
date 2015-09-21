#!/bin/bash

fpm --verbose --force -s dir -t rpm -n avalon-vm -v 2.2 --iteration 4 --license GPL --url http://avalonmediasystem.org --description "Virtual machine distribution setup for Avalon Media System" --rpm-os linux -a noarch --after-install postinst --prefix /usr/share avalon-vm
