from resourses import Server
from resourses import User
import random
import time, datetime


class CommandsHandler():

    options = ["scissors", "paper", "rock"]

    def __init__(self,server):
        assert(isinstance(server, Server.Server))
        self.server = server

    def cmd_whois(self, user):
        return f"Online users: {str([u.nickname for u in self.server.users])}"

    def cmd_count(self, user):
        return f"Online users number: {len(self.server.users)}"

    def cmd_rock_paper_scissors(self, user):
        user.pc_select = random.choice(self.options)
        print(user.pc_select)
        return f"Game started! {self.cmd_count(user)}. Your turn"

    def cmd_rock(self, user):
        chois = 'rock'
        if user.pc_select == chois:
            return f"You both select: {chois}"
        return self.game_action(user, chois)

    def cmd_paper(self, user):
        chois = 'paper'
        if user.pc_select == chois:
            return f"You both select: {chois}"
        return self.game_action(user, chois)

    def cmd_scissors(self, user):
        chois = 'scissors'
        if user.pc_select == chois:
            return f"You both select: {chois}"
        return self.game_action(user, chois)

    def game_action(self, user, chois):
        msg = f"Computer select: {user.pc_select}. You win!" if self.options[self.options.index(chois) - 1] != user.pc_select else f"Computer select: {user.pc_select}. You lose!"
        if not user.pc_select:
            msg = "Please start a game by sending:/rock-paper-scissors"
        user.pc_select = ''
        return msg

    def cmd_time(self, user):
        return str(datetime.datetime.now())

    