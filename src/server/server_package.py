# coding=utf-8

import socketserver
import request_handler
import threading

login_manager=""
loggedin_chars=""

class Server_environment(object):

    def __init__(self, account_manager, active_char,):
        #Save account_manager and active_chars to be reachable at different locations and threads
        global login_manager
        login_manager = account_manager
        global loggedin_chars
        loggedin_chars = active_char
        print("Server environment constructed")

    class PORG_request_handler(socketserver.BaseRequestHandler):
        """ This is base communicator with the client. Each connected client gets 
        one instance of this class in a seperated thread
        """
        def handle(self):
            """This will be done for every connection a client opens.
            """
            logged_user = ""
            client_address = self.client_address[0]
            print ("[%s] created connection" % client_address)
            #Get/Update local variables and setup a message handler for the now created connection
            global loggedin_chars
            message_handler=request_handler.Message_handler(login_manager, self.server, loggedin_chars)
            global login_manager
            login_data = login_manager.get_user()
            #As long as no login was succesful
            while logged_user == "":
                #Wait for identification information from server
                identification = self.request.recv(1024).decode()
                identification = identification.split()
                login_succes = False
                #Search through Accountdata to find a matching set of data
                if identification[0] == "register":
                    message_handler.handle_admin(identification)
                    self.request.send("False".encode('utf-8'))
                else:
                    for acc in login_data:
                        if acc.get_username() == identification[0]  and\
                            acc.get_password() == identification[1]:
                            logged_user=acc
                            print(logged_user.get_username(),"logged in as "\
                            ,logged_user.get_usergroup())
                            self.request.send("True".encode('utf-8'))
                            #Changing login_success to True leaves the while-loop
                            login_succes = True
                    if not login_succes:
                        print("Login unsuccessful")
                        self.request.send("False".encode('utf-8'))
            local_char = request_handler.Character_object(logged_user, [0,0])
            loggedin_chars.add_char(local_char)
            #Infinite loop which takes care of all repeating commands given by the client
            while True:
                message = self.request.recv(1024).decode()
                print(message," recieved from",logged_user.get_username())
                """exit breaks the infinite loops and closes the connection at that way
                Other commands are handled by a special function
                User of the group "su" get a special function
                """
                if message == "exit":
                    loggedin_chars.delete_char(local_char)
                    print("[%s] closed connection" % client_address)
                    break
                #Start admin_handler for special usergroup "su"
                if logged_user.get_usergroup() == "su":
                    message_handler.handle_admin(message)
                    if message == "shutdown":
                        break
                #Otherwise start the normal request_handler
                else : 
                    client_message = message_handler.handle_request(message, logged_user)
                    self.request.send(client_message.encode('utf-8'))


    def start_server(self):
        """ Starts Server and keeps him live until shutdown() command
        """
        porg_server = socketserver.ThreadingTCPServer(("", 50000), 
                                                        self.PORG_request_handler,)
        porg_server.serve_forever()