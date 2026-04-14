class Handlers:
    def __init__(self, bot):
        self.bot = bot
        
    def set_handlers(self, handlers):
        """ Sets bot handlers """
        for handler in handlers:
            self.bot._bot.add_handler(handler)
        print("🔉 Handlers set!")
        
    def add_handler(self, handler):
        """ Adds a single handler to the bot """
        self.bot._bot.add_handler(handler)
        print("🔉 Handler added!")