import boto3


def read(client, b_name, f_name):
    response = client.list_objects_v2(Bucket=b_name, Prefix=f_name)
    for obj in response["Contents"]:
        print(obj)


if __name__ == '__main__':
    s3_client = boto3.client('s3')
    bucket_name = "developer-task"
    folder_name = "y-wing"

    read(s3_client, bucket_name, folder_name)
