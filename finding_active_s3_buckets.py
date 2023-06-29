#The code below will perform the following: 

#It will connect to an AWS environment. 

#It will start reading the S3 bucket files in small portions. 

#If it read a file that was modified within the given timeframes, it will jump to the next bucket. 

#It will only register inactive S3 buckets. 

  

#Imports: 

  

import boto3 

from datetime import datetime 

  

#Variables: 

  

path = "/home/centos/test/buckets_list.txt" 

buckets_list = open(path, "r") 

start_timestamp = datetime(2023, 1, 1) 

end_timestamp = datetime(2023, 7, 1) 

 

#Functions: 

  

def filter_objects(objects): 

    filtered_objects = [] 

    for obj in objects: 

        last_modified = obj['LastModified'] 

        if start_timestamp.date() <= last_modified.date() <= end_timestamp.date(): 

            filtered_objects.append(obj) 

    return filtered_objects 

  

def write_to_file(): 

        with open('inactive_buckets.txt', 'a') as file: 

                file.write(bucket+"\n") 

  

#Environment: (Only if needed) 

  

#os.environ['AWS_ACCESS_KEY_ID'] = '' 

#os.environ['AWS_SECRET_ACCESS_KEY'] = '' 

  

#Logic: 

#We are going to check each of the buckets inside our list recursively if there was any activity in the year of 2023. 

#If we see even a single file created in that year, we move on to the next bucket in the list and so on, if there was no activity in 2023, 

#we are going to write the name of that bucket inside a new file. 

  

while buckets_list: 

        bucket = buckets_list.readline() 

        print("Checking - "+bucket) 

        if bucket == "": break 

        else: 

                s3_client = boto3.client('s3') 

                paginator = s3_client.get_paginator('list_objects_v2') 

                bucket_name = bucket.strip() 

                response_iterator = paginator.paginate(Bucket=bucket_name) 

                for response in response_iterator: 

                        if 'Contents' in response: 

                                filtered_objects = filter_objects(response['Contents']) 

                                if len(filtered_objects) > 0: 

                                        break 

                                if len(filtered_objects) == 0 and response.get('IsTruncated') == False: 

                                        write_to_file() 

                        else: write_to_file() 

buckets_list.close() 
