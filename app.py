import os
import ssl as ssl_lib
import certifi
import logging
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
app = App(token=os.environ["SLACK_BOT_TOKEN"])
roles={}
users={}
channels={}



@app.command("/add-role")
def add_role(ack, body):
    param = body['text'].split()[0]
    if not param in roles:
        ack(f"Adding {param} to Database!")
        roles[param]={
        "name":param,
        "channels": {},
        "users": {}
            }
        ack(f"{param} added to Database!")
    else:
        ack(f"{param} already in database")


@app.command("/list-roles")
def list_roles(ack):
    ack(f"{roles.keys()}")

def print_role(name):
    role=roles[name]
    n=role["name"]
    c=role["channels"]
    u=role["users"]
    msg=f"role: {n}:\n"
    msg+=f"channels: {c}:\n"
    msg+=f"users: {u}:\n"
    return msg

@app.command("/get-role")
def get_role(ack, body):
    param = body['text'].split()[0]
    if not param in roles:
        ack(f"{param} not found")
    else:
        ack(print_role(param))

@app.command("/append-users")
def append_users(ack, body):
    params = body['text'].split()
    role_name = params[0]
    if not role_name in roles:
        ack(f"role: {role_name} not found")
        return
    users = params[1:]
    for u in users:
        roles[role_name]["users"].add(u)
    ack(print_role(role_name))


@app.command("/remove-users")
def remove_users(ack, body):
    params = body['text'].split()
    role_name = params[0]
    if not role_name in roles:
        ack(f"role: {role_name} not found")
        return
    users = params[1:]
    not_found=[]
    for u in users:
        if not u in roles[role_name]["users"]:
            not_found.append(u)
        else:
            roles[role_name]["users"].remove(u)
    ack(f"{print_role(role_name)} \n users already not in role: {not_found}")

@app.command("/append-channels")
def appened_channels(ack, body):
    params = body['text'].split()
    role_name = params[0]
    if not role_name in roles:
        ack(f"role: {role_name} not found")
        return
    channels = params[1:]
    for c in channels:
        roles[role_name]["channels"].add(c)
    ack(print_role(role_name))

@app.command("/remove-channels")
def remove_channels(ack, body):
    params = body['text'].split()
    role_name = params[0]
    if not role_name in roles:
        ack(f"role: {role_name} not found")
        return
    channels = params[1:]
    not_found=[]
    for c in channels:
        if not c in roles[role_name]["channels"]:
            not_found.append(c)
        else:
            roles[role_name]["channels"].remove(c)
    ack(f"{print_role(role_name)} \n channels already not in role: {not_found}")

@app.command("/delete-role")
def delete_role(ack, body):
    param = body['text'].split()[0]
    if param in roles:
        roles.pop(param)
        ack(f"{roles.keys()}")
    else:
        ack(f"{param} is not a role\n{roles.keys()}")


@app.event("app_mention")
def event_test(event, say):
    say(f"Hi there, <@{event['user']}>!")


def ack_shortcut(ack):
    ack()


def open_modal(body, client):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "socket_modal_submission",
            "submit": {
                "type": "plain_text",
                "text": "Submit",
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
            },
            "title": {
                "type": "plain_text",
                "text": "Socket Modal",
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "q1",
                    "label": {
                        "type": "plain_text",
                        "text": "Write anything here!",
                    },
                    "element": {
                        "action_id": "feedback",
                        "type": "plain_text_input",
                    },
                },
                {
                    "type": "input",
                    "block_id": "q2",
                    "label": {
                        "type": "plain_text",
                        "text": "Can you tell us your favorites?",
                    },
                    "element": {
                        "type": "external_select",
                        "action_id": "favorite-animal",
                        "min_query_length": 0,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select your favorites",
                        },
                    },
                },
            ],
        },
    )


app.shortcut("socket-mode")(ack=ack_shortcut, lazy=[open_modal])


all_options = [
    {
        "text": {"type": "plain_text", "text": ":cat: Cat"},
        "value": "cat",
    },
    {
        "text": {"type": "plain_text", "text": ":dog: Dog"},
        "value": "dog",
    },
    {
        "text": {"type": "plain_text", "text": ":bear: Bear"},
        "value": "bear",
    },
]


@app.options("favorite-animal")
def external_data_source_handler(ack, body):
    keyword = body.get("value")
    if keyword is not None and len(keyword) > 0:
        options = [o for o in all_options if keyword in o["text"]["text"]]
        ack(options=options)
    else:
        ack(options=all_options)


@app.view("socket_modal_submission")
def submission(ack):
    ack()

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    roles["hello"]={"name":"hello", "users":{"user1", "user2", "user3"}, "channels":{"c1","c2","c3"}}
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
