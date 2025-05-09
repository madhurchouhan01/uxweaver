def find_chats(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                yield value
            else:
                yield from find_chats(value, target_key)
    elif isinstance(data, list):
        for item in data:
            yield from find_chats(item, target_key)

def find_chats_from_json(data):
    # with open(file) as f:
    #     print("json loaded")
    #     data = json.load(f)
    print("it inside")
    chats = list(find_chats(data, "text"))
    str_result = '\n'.join(chats)
    print(str_result)
    return str_result