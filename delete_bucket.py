import boto3
import json
import gzip
import base64



client = boto3.client('s3')


def lambda_handler(event, context):

    cloudwatch_event = event['awslogs']['data']
    decode_base64 = base64.b64decode(cloudwatch_event)
    decompress_data = gzip.decompress(decode_base64)
    log_data = json.loads(decompress_data)
    print(log_data)


    name = log_data["logEvents"][0]["message"]
    str_dict = json.loads(name)
    bucket_name = str_dict["detail"]["requestParameters"]["bucketName"]


    try:
        response = client.get_bucket_tagging(
        Bucket= bucket_name,
        ExpectedBucketOwner = '090943835041'
        )

        a = response['TagSet'][0]
        x = a["Key"]
        y = a["Value"]
        key = "Environment"
        value = ['dev', 'test', 'UAT', 'production']  # dev, test, UAT and production.

        if 'TagSet' in response:
            if x == key:
                if y == value[0] or y == value[1] or y == value[2] or y == value[3]:
                    print("Environment tag is available")
                    print(a)

            
                else:
                    delete_bucket = client.delete_bucket(
                    Bucket=bucket_name,
                    ExpectedBucketOwner='090943835041'
                    )
                    print("Bucket is deleted")
            
            else:
                delete_bucket = client.delete_bucket(
                Bucket=bucket_name,
                ExpectedBucketOwner='090943835041'
                )
                print("Bucket is deleted")

        else:
            delete_bucket = client.delete_bucket(
            Bucket=bucket_name,
            ExpectedBucketOwner='090943835041'
            )
            print("Bucket is deleted")

        return (response)

    except:

        delete_bucket = client.delete_bucket(
        Bucket=bucket_name,    
        ExpectedBucketOwner='090943835041'
        )
        print("Bucket is deleted")







