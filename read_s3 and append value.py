import json
import boto3


s3_client = boto3.client('s3')

def lambda_handler(event, context):

    bucket_name='datagrokr-devops-technical-assignment-june-2021'
    file_name= 'devops-assignment.json'

    s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    print("s3_response: " ,s3_response)

    file_data = s3_response ["Body"].read().decode('utf')
    print("file_data: " ,file_data)

    json_string = file_data
    a = json.loads(json_string)
    print(type(a))
    a["user"] = "vignesh"
    
    separator = " :"
    b = json.dumps(a, indent=4,separators=(separator))
    print(type(b))

    final_output = b

    s3_client.put_object(Bucket = "bucket2707", Key = "devops.json", Body = str(final_output))


    return (final_output)