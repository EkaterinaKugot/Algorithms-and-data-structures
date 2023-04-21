from enum import Enum
import struct

class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Widget():
    def __init__(self, parent):
        self.parent = parent
        self.childrens = []
        if self.parent is not None:
            self.parent.add_children(self)

    def add_children(self, children: "Widget"):
        self.childrens.append(children)

    def to_binary(self):
        data = b""
        bname = self.__class__.__name__.encode()
        if (self.__class__.__name__ == 'MainWindow'):
            bvalue = self.title.encode()
        elif (self.__class__.__name__ == 'Layout'):
            a = 1
            if self.alignment == Alignment.VERTICAL:
                a = 2
            bvalue = struct.pack("b", a)
        elif (self.__class__.__name__ == 'LineEdit'):
            bvalue = struct.pack("i", self.max_length)
        elif (self.__class__.__name__ == 'ComboBox'):
            if isinstance(self.items[0], int):
                bvalue = struct.pack("i", len(self.items))
            else:
                bvalue = struct.pack("i", 0)
            for i in self.items:
                if isinstance(i, int):
                    bvalue +=  struct.pack("i", i)
                else:
                    bvalue += i.encode()   
        for child in self.childrens:
            bnode=child.to_binary()                
            data += bnode
        result = struct.pack("i", len(bname)) + bname 
        result += struct.pack("i", len(bvalue)) + bvalue + struct.pack("i", len(data)) + data
        return result
    
    @classmethod
    def help_from_binary1(self, data):
        len_name = struct.unpack("i",data[:4])[0]
        name = data[4:4+len_name].decode()
        len_value = struct.unpack("i",data[4+len_name:4+len_name+4])[0]
        value = 0
        if (name == 'MainWindow'):
            value = data[8+len_name:8+len_name+len_value].decode()
        elif (name == 'Layout'):
            value = struct.unpack("b", data[8+len_name:8+len_name+len_value])[0]
            if value == 1:
                value = Alignment.HORIZONTAL
            else:
                value = Alignment.VERTICAL
        elif (name == 'LineEdit'):
            value = struct.unpack("i", data[8+len_name:8+len_name+len_value])[0]
        elif (name == 'ComboBox'):
            value = []
            type_value = struct.unpack("i", data[8+len_name:8+len_name+4])[0]
            len_value1 = len_value - 4
            if type_value == 0:
                    value1 = data[12+len_name:12+len_name+len_value1].decode()
            else:
                i = "i" * type_value
                value1 = struct.unpack(i, data[12+len_name:12+len_name+len_value1])
            for i in value1:
                value.append(i)

        len_childs = struct.unpack("i", data[8+len_name+len_value:8+len_name+len_value+4])[0]
        data_childs = data[12+len_name+len_value:]
        cursor = 0
        current_size = 12+len_name+len_value+len_childs
        
        arr = [name, value]
        while (cursor<len_childs):
            arr2, node_len = Widget.help_from_binary1(data_childs[cursor:])
            arr.append(arr2)
            cursor+=node_len
        return arr, current_size

    @classmethod
    def from_binary(self, data):
        arr = Widget.help_from_binary1(data)[0]
        root = MainWindow(arr[1])
        node1 = Layout(root, arr[2][1])
        node2 = Layout(root, arr[3][1])
        node3 = LineEdit(node1, arr[2][2][1])
        node4 = LineEdit(node1, arr[2][3][1])
        node5 = ComboBox(node2, arr[3][2][1])
        node6 = ComboBox(node2, arr[3][3][1])
        return root


    def __str__(self):
        return f"{self.__class__.__name__}{self.childrens}"

    def __repr__(self):
        return str(self)

class MainWindow(Widget): #корень дерева
    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

class Layout(Widget):
    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

class LineEdit(Widget):
    def __init__(self, parent, max_length: int=10):
        super().__init__(parent)
        self.max_length = max_length

class ComboBox(Widget):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

print(app)

bts = app.to_binary()
print(f"Binary data length {len(bts)}")

new_app = MainWindow.from_binary(bts)
print(new_app)