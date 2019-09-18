from libs.bank import Bank
from plugin import Plugin

class BotPlugin(Plugin):
    def __init__(self, data_dir, bot):
        self.dir = data_dir
        self.bot = bot
        self.currency_name = "doubloons"
        self.betting_pool = 0
        self.bank = Bank()

    # Checks the balance of a user's account
    def balance(self, command):
        user = command.user.username

        if not self.bank.account_exists(user):
            self.bank.create_account(user)

        balance = self.bank.get_balance(user)
        return "CCMP: Hello {}, you have {} {}.".format(user, balance, self.currency_name)

    # Sends currency to another user, subtracting that amount from the sender
    def pay(self, command):
        try:
            parts = command.args.split(" ")

            if not len(parts) == 2:
                return "CCMP: Invalid command format! Please enter /ccpay [user] [amount]."

            from_user = command.user.username
            to_user = parts[0]
            to_user = to_user.strip('@')
            amount = int(parts[1])
        except TypeError:
            return "CCMP: Invalid command format! Please enter /ccpay [user] [amount]."
        except ValueError:
            return "CCMP: Invalid command format! Please enter /ccpay [user] [amount]."

        if amount <= 0:
            return "CCMP: Invalid amount. Please enter a positive value."

        if not self.bank.account_exists(from_user):
            self.bank.create_account(from_user)
        if not self.bank.account_exists(to_user):
            return "CCMP: That account does not exist. Ask them to run /ccbalance."
            
        try:
            if self.bank.charge(from_user, amount):
                if self.bank.pay(to_user, amount):
                    return "CCMP: {} has paid {} {} to {}!".format(from_user, amount, self.currency_name, to_user)
                return "CCMP: Invalid amount of {}. Please enter a positive amount.".format(self.currency_name)
        except TypeError:
            return "CCMP: Invalid command format! Please enter /ccpay @user amount."

    def bet(self, command):
        try:
            user = command.user.username
            amount = int(command.args)

            if self.bank.charge(user, amount):
                self.betting_pool += amount
                return "CCMP: {} has added {} {} to the betting pool".format(user, amount, self.currency_name)
            return "CCMP: You do not possess enough funds."
        except TypeError:
            return "CCMP: Invalid command format! Please enter /ccbet amount."
        except ValueError:
            return "CCMP: Invalid command format! Please enter /ccbet amount."

    def payout(self, command):
        try:
            user = command.user.username
            args = command.args.split(" ")
            to_user = args[0]
            amount = int(args[1])
        except TypeError:
            return "CCMP: Invalid command format! Please enter /ccpayout [user] [amount]."
        except ValueError:
            return "CCMP: Invalid command format! Please enter /ccbet [user] [amount]."

        if user == "Tanner" or user == "Klawk":
            if amount > self.betting_pool or amount <= 0:
                return "CCMP: Invalid amount specified. Must be greater than 0, and less than betting pool."
            if self.bank.account_exists(to_user):
                if self.bank.pay(to_user, amount):
                    self.betting_pool -= amount
                    return "CCMP: Paid {} {} {} from the betting pool.".format(to_user, amount, self.currency_name)
            return "CCMP: That user does not yet have an account. Ask them to check their balance."    
        return "CCMP: You do not have permission to use this command."

    def setname(self, command):
        user = command.user.username
        new_name = command.args

        if user == "Klawk":
            self.currency_name = new_name
            return "CCMP: Currency name changed!"
        return "CCMP: You do not have permission to use this command."

    def on_command(self, command):
        # This method is called when someone types a '/' and one of the commands returned from the set within the get_commands method in this class
        # command is a Command object found within command_wrappers.py
        if command.command == "ccbalance":
            return {"type":"message", "message": self.balance(command)}
        elif command.command == "ccpay":
            return {"type":"message", "message": self.pay(command)}
        elif command.command == "ccbet":
            return {"type":"message", "message": self.bet(command)}
        elif command.command == "ccsetname":
            return {"type":"message", "message": self.setname(command)}
        elif command.command == "ccpayout":
            return {"type":"message", "message": self.payout(command)} 
        elif command.command == "ccpool":
            return {"type":"message", "message": "CCMP: There are currently {} {} in the betting pool".format(self.betting_pool, self.currency_name)}

    def get_commands(self):
        # Must return a set of command strings
        return {"ccbalance", "ccpay", "ccbet", "ccsetname", "ccpayout", "ccpool"}

    def get_name(self):
        # This should return the name of your plugin, perferably the same name as this class
        return "CCMP"

    def get_help(self):
        return "Custom Currancy Management Plug:\n \
                '/ccbalance' to see account balance\n \
                '/ccpay [user] [amount]' to pay a user\n \
                '/ccbet [amount]' to put currency in the betting pool\n \
                '/ccsetname [name]' to change the name of the currency\n \
                '/ccpayout [user] [amount]' to payout from betting pool\n \
                '/ccpool' to see the amount in the betting pool"

    def on_message(self, message):
        # Implementation not required
        return ""

    def has_message_access(self):
        # Implementation not required
        return False
	
    def enable(self):
        pass

    def disable(self):
        pass