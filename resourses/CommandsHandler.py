import random
import datetime


class CommandsHandler:

    @classmethod
    def help(cls, **attrs):
        attrs['user'].post_message("List of available commands:\n"
                                   "/whois - show list of online users\n"
                                   "/count - show number of online users\n"
                                   "/time - show current time\n"
                                   "/game - 'paper-rock-scissors game'")

    @classmethod
    def whois(cls, **attrs):
        attrs['user'].post_message(f"Current online users: {str([u.nickname for u in attrs['obj'].users])}")

    @classmethod
    def count(cls, **attrs):
        attrs['user'].post_message(f"Online users number: {len(attrs['obj'].users)}")

    @classmethod
    def time(cls, **attrs):
        attrs['user'].post_message(str(datetime.datetime.now().strftime('Current time: %H:%M')))

    @classmethod
    def game(cls, **attrs):
        user = attrs['user']
        user.post_message("Let's play! To stop the game type 'stop'. ")
        option = ["scissors", "paper", "rock"]

        while True:
            user.post_message("\nPlease enter your choice: 'scissors', 'paper' or 'rock':")
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
                user.post_message("Well played! Have a good day!")
                break
            else:
                user.post_message("Incorrect choice. You can stop game by typing 'stop'.")
