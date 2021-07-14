# Automate Security Notifications
<p align="center"><img src="images/architecture_diagram.png" width="720" height="290"/>

## Project Overview
This repository demonstrates an automated workflow to send out reminder emails to users at scale using AWS S3, Lambda and Simple Email Service (SES).

## Prerequisite 
To effectively spin up the project using the AWS SAM Framework, you'd require the following prerequisites:
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html)
c
## Set up Guide
**Step 1**: Clone this project into your local environment 

**Step 2**: At the subfolder `automated_security_alerts_sam_app` folder, run `sam build`

**Step 3**: Upon successful build, deploy the project with `sam deploy --guided`

## Author
* Glendon Thaiw ([GitHub](https://github.com/glendont) | [LinkedIn](https://www.linkedin.com/in/glendonthaiw/))

 ## Resources
 * [AWS Serverless Application Model (SAM) Documentation](https://docs.aws.amazon.com/serverless-application-model/index.html) 
 * [Global sections of the AWS SAM Template](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy-globals.html)
 * [Working with AWS Lambda and Lambda Layers in AWS SAM](https://aws.amazon.com/blogs/compute/working-with-aws-lambda-and-lambda-layers-in-aws-sam/)
