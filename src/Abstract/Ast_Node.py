class Ast_Node():

    def __init__(self, value):
        self.__childs = []
        self.__value = value


    def set_child(self, child):
        self.__childs = child

    def add_child(self, value):
        self.__childs.append(Ast_Node(value))

    def add_childs(self, childs):
        for child in childs:
            self.__childs.append(child)

    def add_childs_node(self, child):
        self.__childs.append(child)

    def add_first_child(self, value):
        self.__childs.insert(0, Ast_Node(value))

    def add_first_child_node(self, child):
        self.__childs.inser(0, child)

    def get_value(self):
        return str(self.__value)

    def set_value(self, value):
        self.__value = value

    def get_childs(self):
        return self.__childs

    