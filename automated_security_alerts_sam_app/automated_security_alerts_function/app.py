## Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
## SPDX-License-Identifier: MIT-0

### Importing Relevant Libraries and Packages
import boto3
import numpy as np
import io
import urllib.parse
import os
from io import StringIO
from botocore.exceptions import ClientError
import pandas as pd
from pandas import ExcelWriter
from content import BODY_HTML_PRE


def send_email(RECIPIENT_EMAIL, NAME, NUM_1, NUM_2, NUM_3, BODY_HTML_PRE):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "thaiwg@amazon.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = RECIPIENT_EMAIL

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "RE: [ACTION REQUIRED] Resolve Security Violations"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (
        "Amazon SES Test (Python)\r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto)."
    )

    # Parameters of the email
    NAME = NAME
    DATE = "14 July 2021"
    NUM_VIOLATE_1 = NUM_1
    NUM_VIOLATE_2 = NUM_2
    NUM_VIOLATE_3 = NUM_3

    # The HTML body of the email.
    BODY_HTML_PRE = BODY_HTML_PRE

    BODY_HTML = BODY_HTML_PRE.format(
        NUM_VIOLATE_1=NUM_VIOLATE_1,
        name=NAME,
        NUM_VIOLATE_2=NUM_VIOLATE_2,
        NUM_VIOLATE_3=NUM_VIOLATE_3,
        DATE=DATE,
    )

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client("ses", region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #         ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent to ", RECIPIENT, " at ", DATE)
        print("Email sent! Message ID:"),
        print(response["MessageId"])


def lambda_handler(event, context):
    s3 = boto3.client("s3")

    if event:
        print("Event:", event)
        file_obj = event["Records"][0]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
        print("Key: ", key)
        file_name = key.split("/")[-1]
        file_name_no_suffix = file_name.split(".")[0]
        file_suffix = file_name.split(".")[-1]
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        print("Bucket:", bucket)
        print("Filename:", file_name)
        print("file suffix: ", file_suffix)
        print("Location: ", os.getcwd())

        if file_suffix == "xlsx":
            s3 = boto3.client("s3")
            response = s3.get_object(Bucket=bucket, Key=key)
            data = response["Body"].read()
            sheet_1 = pd.read_excel(
                io.BytesIO(data), sheet_name="mcnconor_2021-06-29_reporting_"
            )
            sheet_2 = pd.read_excel(
                io.BytesIO(data), sheet_name="mcnconor_2021-06-29_patching_"
            )
            sheet_3 = pd.read_excel(
                io.BytesIO(data), sheet_name="mcnconor_2021-06-29_policy_"
            )

            sheet_1 = sheet_1[["primary_owner", "status"]]
            sheet_1 = sheet_1[sheet_1["status"].notna()]
            sheet_1 = sheet_1[sheet_1.status != "GREEN"]
            sheet_1_count = sheet_1.groupby(["primary_owner"]).count()

            sheet_2 = sheet_2[["primary_owner", "status"]]
            sheet_2 = sheet_2[sheet_2["status"].notna()]
            sheet_2 = sheet_2[sheet_2.status != "GREEN"]
            sheet_2_count = sheet_2.groupby(["primary_owner"]).count()

            sheet_3 = sheet_3[["Owner", "Acked"]]
            sheet_3 = sheet_3[sheet_3.Acked == "NO"]
            sheet_3_count = sheet_3.groupby(["Owner"]).count()

            HR_dict = {}
            for i in sheet_1_count.index:
                HR_dict[i] = [sheet_1_count["status"][i], 0, 0]

            for i in sheet_2_count.index:
                if i in HR_dict:
                    HR_dict[i] = [
                        HR_dict[i][0],
                        sheet_2_count["status"][i],
                        HR_dict[i][2],
                    ]
                else:
                    HR_dict[i] = [0, sheet_2_count["status"][i], 0]

            for i in sheet_3_count.index:
                if i in HR_dict:
                    HR_dict[i] = [
                        HR_dict[i][0],
                        HR_dict[i][1],
                        sheet_3_count["Acked"][i],
                    ]
                else:
                    HR_dict[i] = [0, 0, sheet_3_count["Acked"][i]]

            print(HR_dict)

            mock_dict = {"scchia": [1, 4, 5], "thaiwg": [4, 3, 1]}

            for person in mock_dict:
                receipient_email = str(person) + "@amazon.com"
                name = str(person)
                num_1 = mock_dict[person][0]
                num_2 = mock_dict[person][1]
                num_3 = mock_dict[person][2]
                send_email(receipient_email, name, num_1, num_2, num_3, BODY_HTML_PRE)
