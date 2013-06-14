import server_package
import account_manager
import request_handler

"""Standard commands to start the server
"""


print("Server environment is under construction...")
#Server environment gets a instance of Accounter and Active Charlist (with an empty list to start with) for the server
porg_server = server_package.Server_environment(account_manager.Accounter(), request_handler.Active_charlist(list()))
print("Server is starting...")
#Tell the server to start up
porg_server.start_server()
