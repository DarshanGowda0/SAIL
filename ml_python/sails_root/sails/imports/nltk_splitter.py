from pattern.en import parsetree


class ParseTheInput():
    def __init__(self, the_string):
        self.s = parsetree(the_string, relations=True, lemmata=True)

    def find_partition(self):
        tree = self.s
        temp_str = ''
        flag = 0
        for i in tree.words:
            print i.type + ' ' + i.string
            if flag > 0:
                temp_str = temp_str + i.string + ' '
            if i.type == 'VBZ' or i.type == 'WDT' or i.type == 'IN':
                flag += 1
        return temp_str



