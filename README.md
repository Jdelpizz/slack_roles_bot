# Requirements
 - Role consists of a name and users

 - Bot can see all users*
 - Bot can read messages in a roles channel*
 - Bot can send messages in a roles channel*
 - Bot can create a role
 - Bot can list roles
 - Bot can list users from a role
 - Bot can update a role
 - Bot can delete a role
 - Bot can add all users from many roles to many channels*

'*' Requires slack auth


# Adding Bot to slack 
 - Went to `https://api.slack.com/`
 - Clicked `Create an App` -> `From Scratch` -> name: `Roles Bot`

# Adding Bot Auth
 - Went to `https://api.slack.com/`
 - Went to `OAuth & Permissions` on the side bar
 - Went to Scopes -> Add OAuth Scope
 - Added:
  - users:read (see all users in a workspace)
  - channels:history (view messages in channels the bot is added to)
  - chat:write (send messages as bot)
  - channels:manage (manage channels the bot is added to)
 - At the top, under `OAuth Tokens for Your Workspace`, clicked `Install to Workspace`
 - Auth'd Bot and received token

# Adding Bot to Slack
 - In the workspace, went to apps on the left side bar -> `Add Apps` -> Searched `Roles Bot`
 - Added channel called `roles`
 - Sent message `@Roles Bot` in `roles` channel
 - Selected invite button on popup that came

# Created basic bot from References 1

# Subscribing to Events
 - Went to `https://api.slack.com/`
 - Went to `Socket Mode` on the side bar -> Enabled Socket Mode
 - Went to `Event Subscriptions` on the side bar
 - Enabled Events


# References
 - [1] https://github.com/slackapi/python-slack-sdk/blob/main/tutorial/01-creating-the-slack-app.md
