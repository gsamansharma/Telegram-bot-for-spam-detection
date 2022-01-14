from bot import telegram_chatbot
import app
import ban

bot = telegram_chatbot("config.cfg")


def make_reply(msg):
    reply = None
    if msg is not None:
        print(msg)
        reply = app.spmtxt(msg)
    return reply


update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            if "my_chat_member" in item:
                print("nothing")
            else:
                update_id = item["update_id"]
                first_name = item["message"]["from"]["first_name"]
                from_ = item["message"]["chat"]["id"]

                if "new_chat_member" in item["message"]:  # checks if a new member is added
                    print("new")
                    if item["message"]["new_chat_member"]["id"] == 5071047954:  # checks if the new member is bot itself
                        bot.send_message(from_, "Promote me to Admin to avail spam detection feature")
                    else:
                        bot.send_message(from_, "Hello " + item["message"]["new_chat_member"][
                            "first_name"] + " welcome to the group")
                elif "left_chat_member" in item[
                    "message"]:  # not really required but saves the code from getting crashed
                    print("User left")
                else:
                    if item["message"]["chat"]["type"] == "private":
                        bot.send_message(from_, "Use it in a group")
                    else:

                        first_name = item["message"]["from"]["first_name"]
                        # last_name = item["message"]["from"]["last_name"]
                        user_id = item["message"]["from"]["id"]
                        message_id = item["message"]["message_id"]
                        try:
                            message = str(item["message"]["text"])
                            print(type(message))
                            if message.startswith("/start"):
                                # reply="Hello "+first_name+" "+last_name

                                print(message_id)
                                bot.send_reply("Hello " + first_name, message_id, from_)
                            elif message.startswith("/ban"):  #
                                ban_user = item["message"]["reply_to_message"]["from"]["id"]
                                permissions = bot.user_restrict(user_id, from_)
                                permissions = permissions["result"]
                                status = permissions["status"]
                                print(status)
                                if status == "member":
                                    bot.send_reply("You don't qualify excuse him", message_id, from_)
                                else:
                                    bot.ban(ban_user, from_)


                            elif message.startswith("/alive"):
                                # reply="Hello "+first_name+" "+last_name

                                print(message_id)
                                bot.send_reply("Hey " + first_name + ", I am alive ", message_id, from_)


                            elif message.startswith("/excuse"):
                                mercy_user = item["message"]["reply_to_message"]["from"]["id"]
                                permissions = bot.user_restrict(user_id, from_)
                                permissions = permissions["result"]
                                status = permissions["status"]
                                print(status)
                                if status == "member":
                                    bot.send_reply("You don't qualify excuse him", message_id, from_)
                                else:
                                    ban.decreWarnings(str(mercy_user), 1)


                            else:
                                reply = make_reply(message)
                                print(reply)
                                if reply == 1:
                                    chances = ban.getWarnings(str(user_id))
                                    chances = chances - 1
                                    print(chances)
                                    if chances == 0:
                                        bot.send_message(from_, "Long live " + first_name)
                                        bot.ban(user_id, from_)
                                        ban.decreWarnings(str(user_id), 3)
                                    else:
                                        bot.send_reply(
                                            "Attention: That's a spam" + "\n" + "Warnings left: " + str(chances),
                                            message_id, from_)
                        except:
                            message = None
