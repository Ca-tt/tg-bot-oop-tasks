class Languages:
    ENGLISH = 'en'
    SPANISH = 'es'
    FRENCH = 'fr'
    GERMAN = 'de'
    CHINESE = 'zh'
    
    def __init__(self, default_language: str):
        self.supported_languages = {
            self.ENGLISH: "English",
            self.SPANISH: "Spanish",
            self.FRENCH: "French",
            self.GERMAN: "German",
            self.CHINESE: "Chinese"
        }
        self.active_language = default_language
        
    def add_locale(self, locale):
        """ Adds a new locale to the supported languages """
        if locale.code not in self.supported_languages:
            self.supported_languages[locale.code] = locale.name
            print(f"🟢 Locale {locale.name} added!")
        else:
            print(f"⚠️ Locale {locale.name} already exists!")
            
    def set_active_language(self, language_code: str):
        """ Sets the active language for the bot """
        if language_code in self.supported_languages:
            self.active_language = language_code
            print(f"🌐 Active language set to {self.supported_languages[language_code]}!")
        else:
            print(f"❌ Language code {language_code} is not supported!")