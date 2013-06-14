import account_manager

class Message_handler(object):
    """Every Thread of the SocketServer gets a instance of this class it runs in his thread.
    This class is able to understand and interpret all commands given by the client.
    """
    def __init__(self, used_accounter, used_server, active_charlist):
        self.accounter = used_accounter
        self.server = used_server
        self.active_charlist = active_charlist
        
    def handle_request(self, request, logged_user):
        """Handles all requests from normal users. Returns a answer to the client
        """
        request = request.split()
        #Request with a the prefix "position" are move-commands.
        if request[0] == "position":
            #Get the character of the commanding user and his position
            walking_char = self.active_charlist.get_char(logged_user)
            walking_char_pos = walking_char.get_position()
            #Update the position depending on his command (wasd-controls)
            if(request[1] == "w"):
                walking_char_pos[1] += 1
            elif(request[1] == "a"):
                walking_char_pos[0] -= 1
            elif(request[1] == "s"):
                walking_char_pos[1] -= 1
            elif(request[1] == "d"):
                walking_char_pos[0] += 1
        #Return a list of all updated movements.
        active_chars = ""
        for char in self.active_charlist.get_chars():
            active_chars += char.get_user().get_username()+"|"+str(char.get_position()[0])+"|"+str(char.get_position()[1])+"#"
        active_chars += "%"
        return active_chars

    def handle_admin(self, command):
        """Handles all commands from admins"""
        command = command.split()
        #shutdown-command
        if command[0] == "shutdown":
            print("Shutting down server")
            self.server.shutdown()
        #register-user-commandsplit
        if command[0] == "register":
            # Save new user in the accountdada-save-file on the harddisk of the server
            account_file = open("accounts.sav","a")
            account_file.write(command[1]+"|"+command[2]+"|user|")
            account_file.close()
            # Add new user to live list of accountdata.
            self.accounter.add_user(command[1], command[2], "user")

class Character_object(object):
    """Saves data of an active character"""
    def __init__(self, owning_user, start_position):
        super(Character_object, self).__init__()
        self.user = owning_user
        self.position = start_position
        print("Charakter ",self.user.get_username(),"erstellt")
    
    def get_user(self):
        return self.user

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position

class Active_charlist(object):
        """Saving all active chars"""
        def __init__(self, charlist):
            super(Active_charlist, self).__init__()
            self.charlist = charlist
        
        def add_char(self, character_object):
            self.charlist.append(character_object)

        def get_chars(self):
            return self.charlist

        def get_char(self, character):
            for possible_char in self.get_chars():
                if possible_char.get_user() == character:
                    return possible_char
                else:
                    pass