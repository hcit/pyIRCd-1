#!/usr/bin/env python
"""
	USERHOST module for pyIRCd v0.1
"""
import re, sys

# module
module_config = {
	"trigger":"USERHOST",
	"handle":"handle_userhost_request"
}

def handle_userhost_request(client, text):
	try:
		client.reply("RPL_USERHOST", "%s=+%s@%s" % (client.nick, "hidden", client.host))
	except:
		client.reply("ERR_NEEDMOREPARAMS", "Usage: /USERHOST\nYou can only lookup your own nick.")