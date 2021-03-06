#!/usr/bin/env python
"""
	PRIVMSG module for pyIRCd v0.1
"""
import re, sys

valid_mask = "(?P<name>(?P<is_chan>#)?[a-zA-Z0-9\-_]+) :(?P<msg>.+)" # similar to nick allowed mask

# module
module_config = {
	"trigger":"PRIVMSG",
	"handle":"handle_privmsg_request",
	"include channels":True
}

def handle_privmsg_request(client, channels, text):
	target = privmsg_helper(text)
	if target is not None:
		if target["type"] == "channel" and target["name"] in client.channels:
			channel_info = client.channel(target["name"])
			for users in channel_info["users"]:
				# tell everyone on chan about the message
				if users["client"] != client:
					users["client"].connection.send(":%s PRIVMSG %s :%s\n" % (client.nick, target["name"], target["msg"]))
		elif target["type"] == "user":
			user = client.find_user(target["name"])
			if user is not None:
				# deliver the message to target user
				user.connection.send(":%s PRIVMSG %s :%s\n" % (client.nick, target["name"], target["msg"]))
			else:
				client.reply("ERR_NOSUCHNICK", "No such nick/channel")
	else:
		client.reply("ERR_NEEDMOREPARAMS", "invalid msg.")

def privmsg_helper(text):
	target = {}
	target_name = re.search("(%s)" % valid_mask, text) # similar to nick allowed mask
	if target_name is not None:
		target["name"] = target_name.group("name")
		target["msg"] = target_name.group("msg")
		if target_name.group("is_chan") is not None:
			target["type"] = "channel"
		else:
			target["type"] = "user"
		return target
	return None