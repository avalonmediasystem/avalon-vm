#!/bin/bash

fpm --force -s dir -t rpm -n avalon-vm -v 1.1 --iteration 1 --license GPL --url http://avalonmediasystem.org --description "Virtual machine distribution setup for Avalon Media System" --rpm-os linux -a noarch --after-install postinst --prefix /usr/share avalon-vm
