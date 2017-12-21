class Cleaner:
    def __init__(self, data_set):
        self.name_field_list = ['first name', 'last name']
        self.name_field = {}
        self.data_set = data_set
        header = data_set[0]
        for i in range(len(header)):
            if header[i] in self.name_field_list:
                self.name_field[header[i]] = i

    def trim_name(self):
        for i in range(1, len(self.data_set)):
            for j in self.name_field:
                index = self.name_field[j]
                self.data_set[i][index] = self.data_set[i][index].strip()

    def exchange_name(self):
        for i in range(1, len(self.data_set)):
            for j in self.name_field:
                if j == 'first name':
                    first_index = self.name_field[j]
                if j == 'last name':
                    last_index = self.name_field[j]
            temp = self.data_set[i][first_index]
            self.data_set[i][first_index] = self.data_set[i][last_index]
            self.data_set[i][last_index] = temp

    def upper_name(self):
        for i in range(1, len(self.data_set)):
            for j in self.name_field:
                index = self.name_field[j]
                self.data_set[i][index] = self.data_set[i][index].upper()