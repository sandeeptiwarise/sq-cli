from sqlient import SQlient


class SQCLI:
    def __init__(self):
        pass


if __name__ == '__main__':
    client_michal = SQlient("michal", "3.121.232.99:9000", "minioadmin", "minioadmin")
    client_michal.qrypt.encrypt_file("data/file1.txt")
    client_michal.mount10.put_object(client_michal.buckets[0], "file1", "data/file1.txt")
