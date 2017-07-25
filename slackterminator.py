import json
import os
from slackclient import SlackClient
import time

slack_token = os.environ["SLACK_API_TOKEN"]
slack_client = SlackClient(slack_token)

#Delay as suggested by Slack team. Faster might work, but risk being throttled/blocked.
ratelimit_delay_s = 1

def get_messages (channel_name, pagination_count=1000):
	channel_id = get_channel_id(channel_name)
	print "retrieving message history of channel: " + channel_name + ", " + channel_id
	response = slack_client.api_call(
	  "channels.history",
	  channel=channel_id,
	  count=pagination_count,
	)
	messages = response ["messages"]
	return messages


def delete_message (channel_id, timestamp):
	print "deleting message at timestamp: " + timestamp 
	response = slack_client.api_call(
	  "chat.delete",
	  channel=channel_id,
	  ts=timestamp
	)
	print response

def delete_all_messages (channel_name):
	messages = get_messages(channel_name)
	channel_id = get_channel_id(channel_name)
	for message in messages:
		timestamp = message["ts"]
		print "deleting message at timestamp: " + timestamp 
		response = slack_client.api_call(
		  "chat.delete",
		  channel=channel_id,
		  ts=message["ts"]
		)
		print response
		time.sleep(ratelimit_delay_s)

# Returns all channel objects in JSON format
def get_channels ():
	response = slack_client.api_call(
	  "channels.list"
	)
	channels = response["channels"]
	return channels

def get_channel_id (channel_name):
	channels = get_channels()
	for channel in channels:
		if channel["name"] == channel_name:
			return channel["id"]

delete_all_messages("general")