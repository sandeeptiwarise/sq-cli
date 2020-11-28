class SQCLI:
    def __init__(self):
        pass


if __name__ == '__main__':
    sqrypt = SQrypt()
    bucket = sqrypt.create_bucket("jonatan")
    sqrypt.upload_file(bucket, "file1.txt", "data/file1.txt")
