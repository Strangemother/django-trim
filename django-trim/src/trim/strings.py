import hashlib



def str_to_hex(str_content):
    return bytes_to_hex(bytes(str_content, 'utf'))


def bytes_to_hex(bytes_content):
    return hashlib.sha1(bytes_content).hexdigest()
