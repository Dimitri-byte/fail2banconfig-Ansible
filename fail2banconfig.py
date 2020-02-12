#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2020, Dimitri Biard <biarddimitri@gmail.com>
# GNU General Public License V3.0+ (see COPYING or https://www.gnu.org/license/glp-3.0.txt)

DOCUMENTATION='''
module: fail2banconfig
author: Dimitri Biard
description: This module creates a basic config file for Fail2ban in /etc/fail2ban/jail.d/custom.conf. For more information about Fail2ban you can check <https://fail2ban.org/wiki/index.php/Main_page>

option:
  ignoreip:
    description: to ignore specific Ips. By default 127.0.0.1.
    required: false
  findtime:
    description: The length of time between login attempts beforea ban is set. By default 3600 sec.
    required: false
  bantime:
    description: The length of time in seconds for which an IP is banned. by default 86400 sec.
    required: false
  maxretry:
    description: How many attempts can be made to access the server from a single IP before a ban is imposed. By default 3 times.
    required: false
  services:
    description: Add many services. Use the symbole "$" to allow a line break.
    required: false
'''
EXAMPLES='''
- name: "fail2ban ssh minimum configuration"
  fail2banconfig:
    service = "$[sshd]
               $enabled = true"

- name: "fail2ban ssh custom configuration"
  fail2banconfig:
    ignoreip = "127.0.0.1 10.10.0.1 10.10.0.2"
    fintime = "5000"
    bantime = "600"
    maxretry = "5"
    services = "$[sshd]
                $enabled = true
                $logpath = /var/log/auth.log"
'''
RETURN='''#'''

################## VARIABLES  ###########################

path = "/etc/fail2ban/jail.d/custom.conf"

##################   IMPORT   ###########################

from ansible.module_utils.basic import AnsibleModule
import os
##################  FUNCTIONS ###########################

# This function creates the the file custom.conf and write
# basic arguments.
def customfile(ignoreip, findtime, bantime, maxretry):
	# Create the file
	custom = open(path, "w")

	# Write basic arguments

	custom.write("[DEFAULT]")

	# ignoreip
	custom.write("\nignoreip = ")
	custom.write(ignoreip)

	# findtime
	custom.write("\nfindtime = ")
	custom.write(findtime)

	# bantime
	custom.write("\nbantime = ")
	custom.write(bantime)

	# maxretry
	custom.write("\nmaxretry = ")
	custom.write(maxretry)
	custom.write("\n")


	#Close file
	custom.close()

# This function add service's arguments
def customserv(serv):
	if serv != None:
		custom = open(path, "a")
		for i in serv:
			if i == "$":
				custom.write("\n")
			else:
				custom.write(i)
		custom.close

	else:
		return "No service"

##################  PROGRAM START  ######################

# Main function
def main():
	# Call AnsibleModule to create arguments for playbook.
	module = AnsibleModule(
		argument_spec=dict(
		ignoreip   = dict(default="127.0.0.1", type='str'),
		findtime   = dict(default="3600", type='str'),
		bantime    = dict(default="86400", type='str'),
		maxretry   = dict(default="3", type='str'),
		services   = dict(default=None, type='str'),

		)
	)

	# Call customfile() to create the config file an write basic arguments
	ip = module.params['ignoreip']
	ft = module.params['findtime']
	bt = module.params['bantime']
	rt = module.params['maxretry']

	customfile(ip, ft, bt, rt)

	# Call customserv() and add service's arguments
	sv = module.params['services']

	customserv(sv)

	# Restart fail2ban to apply settings
	os.system("systemctl restart fail2ban")

##################   DEBUG    ###########################

	resultat = module.params['services']
	debug = 0

##################    END     ###########################
	module.exit_json(changed=False, debug=resultat)


if __name__ == "__main__":
	main()
