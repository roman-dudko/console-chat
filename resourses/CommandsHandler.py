from resourses import Server
import random
import datetime


class CommandsHandler():

    options = ["scissors", "paper", "rock"]
    invite = "Please enter your choice: '/scissors', '/paper' or '/rock':"

    def __init__(self,server):
        assert(isinstance(server, Server.Server))
        self.server = server

    def cmd_whois(self, user):
        return f"Current online users: {str([u.nickname for u in self.server.users])}"

    def cmd_count(self, user):
        return f"Online users number: {len(self.server.users)}"

    def cmd_game(self, user):
        user.pc_select = random.choice(self.options)
        print(f"Game started. Server choice: {user.pc_select}")
        return f"Let's play! {self.invite}"

    def cmd_rock(self, user):
        choice = 'rock'
        return self.game_action(user, choice)

    def cmd_paper(self, user):
        choice = 'paper'
        return self.game_action(user, choice)

    def cmd_scissors(self, user):
        choice = 'scissors'
        return self.game_action(user, choice)

    def cmd_stop_game(self, user):
        user.pc_select = ""
        return "Well played! Have a good day!"

    def game_action(self, user, choice):
        if not user.pc_select:
            user.pc_select = random.choice(self.options)
            msg = f"Ooops. Server not ready.{self.invite}"
            return msg

        if user.pc_select == choice:
            msg = f"We both select: {choice}."
        else:
            msg = f"Computer select: {user.pc_select}. You win!" if self.options[self.options.index(choice) - 1] != \
                                                                user.pc_select else f"Computer select: " \
                                                                                    f"{user.pc_select}. You lose! " \
                                                                                    f"Better luck next time!"
        user.pc_select = random.choice(self.options)
        msg += f" One more time?\n{self.invite}"
        return msg

    def cmd_time(self):
        return str(datetime.datetime.now())

