import cmd
import sys
import logging
import boto3
from botocore.exceptions import ClientError


class CLI(cmd.Cmd):
    prompt = ">> "

    def do_list(self, arg):
        read(s3_client, bucket_name, folder_name)

    def do_upload(self, arg):
        try:
            add(s3_client, bucket_name, arg)
            print(f"{arg} successfully added to the bucket.")
        except ClientError as e:
            logging.error(e)

    def do_find(self, arg):
        print(arg)
        find(s3_client, bucket_name, "y-wing/", arg)
        print(arg)


def read(client, b_name, f_name):
    response = client.list_objects_v2(Bucket=b_name, Prefix=f_name)
    for obj in response["Contents"]:
        print(obj)


def add(client, b_name, file):
    client.upload_file(file, b_name, "y-wing/" + file)


def find(client, b_name, f_name, r=""):
    response = client.list_objects_v2(Bucket=b_name, Prefix=f_name + r)
    for obj in response["Contents"]:
        print(obj)


if __name__ == '__main__':
    s3_client = boto3.client('s3')
    bucket_name = "developer-task"
    folder_name = "y-wing"

    CLI().cmdloop()

