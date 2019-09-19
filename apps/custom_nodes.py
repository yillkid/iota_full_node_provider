list_custom_nodes = []

def load_custom_nodes():
    file_input = open("input/input.txt","r")
    list_custom_nodes = file_input.readlines()
    file_input.close()

    return list_custom_nodes
