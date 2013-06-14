
class Userobject(object):
    """Each user is represented by one Userobject, which saves his personal
    data. All Userobjects are saved in the Accounter class and available for
    other functions from there.
    """
    def __init__(self, username, password, usergroup):
        self.name = username
        self.passwd = password
        self.group = usergroup

    def get_username(self):
        return self.name

    def get_password(self):
        return self.passwd

    def get_usergroup(self):
        return self.group

class Accounter(object):
    """Accounter reads all accounts from the accountfile/database saved on the
    hard disk of the server during its initialization. The account data is 
    saved in a set of Userobjects with are accessable through the methods of
    this class.
    """

    def __init__(self):
        print("Unpacking saved accountdata...")
        acc_file = open("accounts.sav","r")
        input_accounts = list()
        #Accounts are saved in the format username|password|group
        for line in acc_file:
            input_accounts.append(line.split("|"))
        acc_file.close()
        self.accountset = set()
        print("Saving Accounts...")
        for account in input_accounts:
            new_user=(Userobject(account[0],account[1],account[2]))
            self.accountset.add(new_user)
        #Giving feedback on the server terminal
        for acc in self.accountset: 
            print(acc.get_username()," saved with password ",\
            acc.get_password()," in the group ",\
            acc.get_usergroup())
        print("Accountmanager initialized")

    def get_user(self):
        return self.accountset

    def add_user(self, new_user, user_password, group):
        new_userobject=(Userobject(new_user, user_password, group))
        self.accountset.add(new_userobject)
        print(new_user,"with password",user_password,"in group",group,"created")
