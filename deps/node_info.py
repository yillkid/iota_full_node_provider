from iota import Iota

def get_milestoneStartIndex(url):
    try:
        api = Iota(url)
        node_info = api.get_node_info()
        return int(node_info["milestoneStartIndex"])

    except:
        return 0
