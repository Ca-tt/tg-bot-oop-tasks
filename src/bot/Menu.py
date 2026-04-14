class Menu:
    # bot sidebar menu manager, sets menu commands and handlers for them
    def __init__(self, bot):
        self.bot = bot
        self.menu_commands = None # get commands from languages or config
        
    def set_menu_commands(self):
        """ Sets bot menu commands """
        # get menu commands from languages or config and set them for the bot
        
        print("🔉 Slash commands set!")
        
        