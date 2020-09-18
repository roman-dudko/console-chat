import random
import datetime


class CommandsHandler:

    @classmethod
    def help(cls, obj, user):
        user.post_message("List of available commands:\n"
                          "/whois - show list of online users\n"
                          "/count - show number of online users\n"
                          "/time - show current time\n"
                          "/game - 'paper-rock-scissors game'")

    @classmethod
    def whois(cls, obj, user):
        user.post_message(f"Current online users: {str([u.nickname for u in obj.users])}")

    @classmethod
    def count(cls, obj, user):
        user.post_message(f"Online users number: {len(obj.users)}")

    @classmethod
    def time(cls, obj, user):
        user.post_message(str(datetime.datetime.now().strftime('Current time: %H:%M')))

    @classmethod
    def game(cls, obj, user):
        user.post_message(f"Let's play! To stop the game type 'stop'. ")
        option = ["scissors", "paper", "rock"]

        while True:
            user.post_message(f"\nPlease enter your choice: 'scissors', 'paper' or 'rock':")
            user_select = user.get_message(1024)
            if user_select in ("scissors", "paper", "rock"):
                pc_select = random.choice(option)
                if pc_select == user_select:
                    user.post_message(f"We both select {pc_select}. Let's try again!")
                elif option[option.index(user_select) - 1] != pc_select:
                    user.post_message(f"Your {user_select} vs my {pc_select}. "
                                      f"You win! One more time?")
                else:
                    user.post_message(f"Your {user_select} vs my {pc_select}. "
                                      f"You lose! Better luck next time!")
            elif user_select == "stop":
                user.post_message(f"Well played! Have a good day!")
                break
            else:
                user.post_message(f"Incorrect choice. You can stop game by typing 'stop'.\n")