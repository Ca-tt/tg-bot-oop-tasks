class Stats:
    """ collect user-related statistics, such as average score, max score, etc. """
    def __init__(self, name):
        self.name = name
        self.data = []
        
    def add_data(self, value):
        self.data.append(value)
        
    def get_average(self):
        if not self.data:
            return 0
        return sum(self.data) / len(self.data)
    
    def get_max(self):
        if not self.data:
            return 0
        return max(self.data)
    
    def get_min(self):
        if not self.data:
            return 0
        return min(self.data)
    
    def get_count(self):
        return len(self.data)