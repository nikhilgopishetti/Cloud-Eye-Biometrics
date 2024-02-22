import boto3
import io
from PIL import Image

def authenticateimage(uploaded_image):
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    image_path = uploaded_image

    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()


    response = rekognition.search_faces_by_image(
            CollectionId='employees-images',
            Image={'Bytes':image_binary}                                       
            )

    found = False
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])
            
        face = dynamodb.get_item(
            TableName='employees',  
            Key={'rekognitionid': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face:
            print ("Found Person: ",face['Item']['firstName']['S'])
            found = True

    if not found:
        print("Person cannot be recognized")


def upload_image_to_s3(file_path, bucket_name, object_name):
    """
    Uploads an image file to an S3 bucket.
    
    Args:
        file_path (str): The local file path of the image to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The name to give the object in the S3 bucket.
        
    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, object_name)
        print("Upload successful!")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False