import cmd
import sys
import logging
import boto3
from botocore.exceptions import ClientError


class CLI(cmd.Cmd):
    prompt = ">> "
    intro = "AWS-project. Type 'help' for available commands."

    def do_list(self, arg):
        """
        List all files in bucket. (folder hardcoded)
        Use -a for -all flag to display all object information.
        """
        read(s3_client, bucket_name, folder_name, arg)

    def do_upload(self, arg):
        """
        Upload file to the bucket.
        """
        try:
            add(s3_client, bucket_name, arg)
            print(f"{arg} successfully added to the bucket.")
        except ClientError as e:
            logging.error(e)

    def do_find(self, arg):
        """
        Find files that starts with a argument.
        Didn't know how to implement an actual regex so it only works as a prefix.
        """
        find(s3_client, bucket_name, "y-wing/", arg)

    def do_delete(self, arg):
        """
        Delete single file.
        """
        delete(s3_client, bucket_name, "y-wing/" + arg)

    def do_purge(self, arg):
        """
        Delete all files that starts with an argument.
        """
        delete_all(s3_client, bucket_name, "y-wing/", arg)

    def do_quit(self, arg):
        """
        Exit
        """
        return True


def read(client, b_name, f_name, *args):
    response = client.list_objects_v2(Bucket=b_name, Prefix=f_name)
    if "-a" in args[0] or "-all" in args[0]:
        for obj in response["Contents"]:
            print(obj)
    else:
        for obj in response["Contents"]:
            print(obj["Key"])


def add(client, b_name, file):
    client.upload_file(file, b_name, "y-wing/" + file)


def delete(client, b_name, file):
    response = client.delete_object(Bucket=b_name, Key=file)
    print(response)


def delete_all(client, b_name, folder, r=""):
    if r == "":
        print("Please specify file prefix.")
    else:
        response = client.list_objects_v2(Bucket=b_name, Prefix=folder + r)
        try:
            totals = len(response["Contents"])
            for obj in response["Contents"]:
                name = obj["Key"]
                client.delete_object(Bucket=b_name, Key=name)
                print(f"{name}, deleted.")
            print(f"-- Deleted {totals} files. --")
        except Exception as e:
            logging.error(e)
            print(f"No files starts with {r}.")


def find(client, b_name, f_name, r=""):
    response = client.list_objects_v2(Bucket=b_name, Prefix=f_name + r)
    try:
        for obj in response["Contents"]:
            print(obj["Key"])
    except Exception as e:
        logging.error(e)
        print(f"No file starts with {r}.")


if __name__ == '__main__':
    s3_client = boto3.client("s3")
    bucket_name = "developer-task"
    folder_name = "y-wing"

    CLI().cmdloop()

