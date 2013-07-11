Dies ist das Github-Repository zu dem Online Projekt "PORG". Für mehr Informationen siehe adyouki-go.org

This is the Github-Repository of the online project "PORG". For further information read adyouki-go.org

=====index=====

====src====

===server===
Here are all files which have to be stored on the server

==account_manager==
All classes and documents to manage accounts are located here.
This currently includes the >Accounter<, which is the main class with the accounting logic and the >Userobject< which saves all data for one User
==accounts.sav==
This is used to save all account data on the hard disk. Accounts are saved in the format "username|password|usergroup"
This should be replaced by a database !
==init_server.py==
This is a small script which calls all functions needed to start a server instance.

==request_handler==
All basic logic to handle a request from the client is here.
This includes the >Message_handler<, which is called by the SocketThreads to process a ingoing request, the >Character_object<, which saves all data of a ingame character and the >Active_charlist< which is a list of all characters which are currently online.

==server_package==
This is the basic code, which handles the server and the communiction with the client.
This includes the Server_environment which constructs and links everything a working client instance needs. The PORG_request_handler is a class which gets started as an extra thread for every incoming connection from a client and manages the communiction between client and server.

===client===
Here are all files needed to setup a client.

==admin_client==
This is the client for admin access to the server.
Adminuser: Name "admin" password "superpassword"
Working commands are:
-"register [username] [password]" : Registers [username] with [password]
-"shutdown" : Shuts the server down.

==game_client== (depricated)
pygame_client is a newer version of this which uses pygame for keyboard events to control characters.
This is the client a player uses to access the server
Later this client and his side classes should handle the physics of the game to save the server from workload.
Currently registered users: Name "Testuser" password "Test"
The user can move his character with the input of "w","a","s" and "d" (common wasd-controls)

==pygame_client==
pygame_client is a newer version of pygame_client which uses pygame for keyboard events to control characters.
This is the client a player uses to access the server
Later this client and his side classes should handle the physics of the game to save the server from workload.
Currently registered users: Name "Testuser" password "Test"
The user can move his character with pressing of "w","a","s" and "d" after login(common wasd-controls)

==shutdown_script==
This is a short script which logs in as admin and shutdowns the server.
This only for testing and should not be used for the actual productive system.
