"""
Contains user data to access data from Notion account / API
"""

# INSERT OWN VALUES (replace TODO with your keys from Notion)
class User:
	# Official docu for Notion API access token:
	# https://developers.notion.com/docs/authorization
	access_token = "TODO"
	# How to get the block id of a table:
	# https://stackoverflow.com/questions/67618449/how-to-get-the-block-id-in-notion-api
	daily_block_id = "TODO"
	general_block_id = "TODO"
	notes_block_id = "TODO"
	