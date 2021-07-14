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

def send_email(RECIPIENT_EMAIL, NAME, NUM_1, NUM_2, NUM_3):
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
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )

    # Parameters of the email
    NAME = NAME
    DATE="14 July 2021"
    NUM_VIOLATE_1 = NUM_1
    NUM_VIOLATE_2 = NUM_2
    NUM_VIOLATE_3 = NUM_3

    # The HTML body of the email.
    BODY_HTML_PRE = """
    <html xmlns:v="urn:schemas-microsoft-com:vml"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:w="urn:schemas-microsoft-com:office:word"
    xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"
    xmlns="http://www.w3.org/TR/REC-html40">

    <head>
    <meta http-equiv=Content-Type content="text/html; charset=unicode">
    <meta name=ProgId content=Word.Document>
    <meta name=Generator content="Microsoft Word 15">
    <meta name=Originator content="Microsoft Word 15">
    <link rel=File-List
    href="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/filelist.xml">
    <link rel=Edit-Time-Data
    href="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/editdata.mso">

    <link rel=themeData
    href="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/themedata.thmx">
    <link rel=colorSchemeMapping
    href="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/colorschememapping.xml">

    <style>
    </style>

    </head>

    <body lang=EN-US link="#0563C1" vlink="#954F72" style='tab-interval:36.0pt'>

    <div class=WordSection1>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    <p class=MsoNormal><a name="_Hlk76117587"></a><a name="_Hlk76048917"><span
    style='mso-bookmark:_Hlk76117587'>Dear <span style='background:yellow;
    mso-highlight:yellow'>{name}</span>,</span></a></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><o:p>&nbsp;</o:p></span></span></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'>This email is sent to SAs who have breached
    the Security Expectations to ensure full compliance with the following:</span></span></p>

    <ol style='margin-top:0cm' start=1 type=1>
     <li class=MsoListParagraphCxSpFirst style='margin-left:-18.0pt;mso-add-space:
         auto;mso-list:l2 level1 lfo1'><span style='mso-bookmark:_Hlk76048917'><span
         style='mso-bookmark:_Hlk76117587'><span style='mso-fareast-font-family:
         "Times New Roman"'>NAWS patch reporting is at 100% compliance<o:p></o:p></span></span></span></li>
     <li class=MsoListParagraphCxSpMiddle style='margin-left:-18.0pt;mso-add-space:
         auto;mso-list:l2 level1 lfo1'><span style='mso-bookmark:_Hlk76048917'><span
         style='mso-bookmark:_Hlk76117587'><span style='mso-fareast-font-family:
         "Times New Roman"'>Team’s patching should have 0 Red (SLA violation)<o:p></o:p></span></span></span></li>
     <li class=MsoListParagraphCxSpLast style='margin-left:-18.0pt;mso-add-space:
         auto;mso-list:l2 level1 lfo1'><span style='mso-bookmark:_Hlk76048917'><span
         style='mso-bookmark:_Hlk76117587'><span style='mso-fareast-font-family:
         "Times New Roman"'>S3 Block Public Access (BPA) alerts and<o:p></o:p></span></span></span></li>
    </ol>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'>As of <span style='background:yellow;
    mso-highlight:yellow'>{DATE}</span>, these are the violations related to your
    account:</span></span></p>

    <table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0
     style='margin-left:-.25pt;border-collapse:collapse;mso-yfti-tbllook:1184;
     mso-padding-alt:0cm 0cm 0cm 0cm'>
     <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes'>
      <td width=255 valign=top style='width:191.4pt;border:solid windowtext 1.0pt;
      background:#AEAAAA;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Type of Violation<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=180 valign=top style='width:134.65pt;border:solid windowtext 1.0pt;
      border-left:none;background:#AEAAAA;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Number of Violations<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=189 valign=top style='width:141.7pt;border:solid windowtext 1.0pt;
      border-left:none;background:#AEAAAA;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>To be Addressed<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:1'>
      <td width=255 valign=top style='width:191.4pt;border:solid windowtext 1.0pt;
      border-top:none;background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>NAWS Patch Reporting</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=180 valign=top style='width:134.65pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span style='background:yellow;mso-highlight:
      yellow'>{NUM_VIOLATE_1}</span></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=189 valign=top style='width:141.7pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Immediately<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:2'>
      <td width=255 rowspan=2 valign=top style='width:191.4pt;border:solid windowtext 1.0pt;
      border-top:none;background:#FFE599;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Red (violation of patching SLA)</span></span></p>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Yellow (in need of patching)</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=180 rowspan=2 valign=top style='width:134.65pt;border-top:none;
      border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#FFE599;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span style='background:yellow;mso-highlight:
      yellow'>{NUM_VIOLATE_2}</span></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=189 valign=top style='width:141.7pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#FFE599;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Immediately<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:3'>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=189 valign=top style='width:141.7pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#FFE599;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Before they fall out of SLA</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:4;mso-yfti-lastrow:yes'>
      <td width=255 valign=top style='width:191.4pt;border:solid windowtext 1.0pt;
      border-top:none;background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Not acknowledging/remediating S3 Block
      Public Access (BPA) alerts</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=180 valign=top style='width:134.65pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span style='background:yellow;mso-highlight:
      yellow'>{NUM_VIOLATE_3}</span></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=189 valign=top style='width:141.7pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      background:#F2F2F2;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Immediately<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
    </table>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'>SA leaders can also check the security
    dashboard to see the latest stats by clicking on reporting, and scrolling down
    to see the status for your directs: </span></span><a
    href="https://security-dashboard.aws.a2z.com/dashboards/permalink/patching"><span
    style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
    lang=EN-SG style='mso-ansi-language:EN-SG'>https://security-dashboard.aws.a2z.com/dashboards/permalink/patching</span></span></span><span
    style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
    style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><u><span
    lang=EN-SG style='color:#0563C1;mso-ansi-language:EN-SG'><o:p></o:p></span></u></span></span></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><o:p>&nbsp;</o:p></span></span></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'>To resolve these common policy violations,
    you may refer to the resources below. It should take you less than 10 minutes
    to complete.</span></span></p>

    <table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0
     style='border-collapse:collapse;mso-yfti-tbllook:1184;mso-padding-alt:0cm 0cm 0cm 0cm'>
     <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      background:#AEAAAA;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Policy Violation<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border:solid windowtext 1.0pt;
      border-left:none;background:#AEAAAA;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b>Steps to Resolve<o:p></o:p></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:1'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>NAWS Patch Reporting</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Refer to </span></span><a
      href="https://quip-amazon.com/JrG9AKPbgOFs/PVRE-NAWS-Patching-using-SSM"><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'>https://quip-amazon.com/JrG9AKPbgOFs/PVRE-NAWS-Patching-using-SSM</span></span><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'> </span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:2'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Red hosts</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Address</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:3'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Yellow hosts</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Address</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:4'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Open Risks for S3 Bucket</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>Ensure your S3 Block Public Access (BPA) alerts are
      acknowledged/remediated: <o:p></o:p></span></span></span></p>
      <ul style='margin-top:0cm' type=disc>
       <li class=MsoListParagraph style='margin-bottom:0cm;margin-left:0cm;
           margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;mso-list:
           l7 level1 lfo2'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://policyengine.amazon.com/"><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>https://policyengine.amazon.com/</span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'> Choose “Security Risk” next to your name. <o:p></o:p></span></span></span></li>
      </ul>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>

      <![if !vml]>

      <img border=0 width=457 height=104
      src="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/image002.gif"
      style='height:1.083in;width:4.756in' v:shapes="_x0000_i1026"><![endif]></span></span></span></p>
      <ul style='margin-top:0cm' type=disc>
       <li class=MsoListParagraphCxSpFirst style='margin-bottom:0cm;margin-left:
           0cm;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l7 level1 lfo2'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Expand Account S3 BPA
           Disabled to see who in your team has open risks for public S3 buckets<o:p></o:p></span></span></span></li>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           0cm;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l7 level1 lfo2'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Ask your teams to acknowledge
           the risk in the PolicyEngine and either<o:p></o:p></span></span></span></li>
       <ul style='margin-top:0cm' type=circle>
        <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
            0cm;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
            mso-list:l7 level2 lfo2'><span style='mso-bookmark:_Hlk76048917'><span
            style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
            "Times New Roman";mso-ansi-language:EN-SG'>Set a remediation date and
            remediate the public access or<o:p></o:p></span></span></span></li>
        <li class=MsoListParagraphCxSpLast style='margin-bottom:0cm;margin-left:
            0cm;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
            mso-list:l7 level2 lfo2'><span style='mso-bookmark:_Hlk76048917'><span
            style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
            "Times New Roman";mso-ansi-language:EN-SG'>State why this public access
            is required by design (this is completely acceptable if it complies
            with the Secure Engagement guidelines)<o:p></o:p></span></span></span></li>
       </ul>
      </ul>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><o:p>&nbsp;</o:p></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:5;mso-yfti-lastrow:yes'>
      <td width=123 valign=top style='width:91.9pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>Other Resources</span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=501 valign=top style='width:375.6pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'>For guidance on common difficult scenarios,
      refer to </span></span><a
      href="https://w.amazon.com/bin/view/AWS/VM/NAWS/Challenges_and_Guidance/"><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'>https://w.amazon.com/bin/view/AWS/VM/NAWS/Challenges_and_Guidance/</span></span><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
      style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></p>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><o:p>&nbsp;</o:p></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
    </table>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><o:p>&nbsp;</o:p></span></span></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
    EN-SG'>In the future, please keep track of these violations which you can do so
    by making use of the tools that monitor your Isengard accounts:<o:p></o:p></span></span></span></p>

    <table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0
     style='border-collapse:collapse;mso-yfti-tbllook:1184;mso-padding-alt:0cm 0cm 0cm 0cm'>
     <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes'>
      <td width=274 valign=top style='width:205.3pt;border:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>Tools<o:p></o:p></span></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=350 valign=top style='width:262.2pt;border:solid windowtext 1.0pt;
      border-left:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><b><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>Action to Take<o:p></o:p></span></b></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:1'>
      <td width=274 valign=top style='width:205.3pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=1 type=1>
       <li class=MsoListParagraphCxSpFirst style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l1 level1 lfo3'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Policy Engine is an overall
           dashboard of the security posture of your AWS account. It sends a weekly
           email (which all of you have been subscribed) about risks in your
           account. <o:p></o:p></span></span></span></li>
      </ol>
      <ul style='margin-top:0cm' type=disc>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l0 level1 lfo4'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>L</span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           style='mso-fareast-font-family:"Times New Roman"'>inks: </span></span></span><a
           href="https://w.amazon.com/bin/view/PolicyEngine/Home"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>wiki</span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>, </span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://policyengine.amazon.com/"><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>tool</span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'><o:p></o:p></span></span></span></li>
      </ul>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=350 valign=top style='width:262.2pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=1 type=a>
       <li class=MsoListParagraphCxSpLast style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l5 level1 lfo5'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>If you get an email with
           issues from Policy Engine, you should <b>acknowledge them</b>, and put a
           <b>target date for compliance</b>. The most common check that surfaces
           in Policy Engine is that the AWS Account-wide “S3 Block Public Access”
           is not enabled.<o:p></o:p></span></span></span></li>
      </ol>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
      EN-SG'><o:p>&nbsp;</o:p></span></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:2'>
      <td width=274 valign=top style='width:205.3pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=2 type=1>
       <li class=MsoListParagraphCxSpFirst style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l1 level1 lfo3'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Palisade is a tool that runs
           certain security checks and <b>will cut a TT</b> if it finds a
           violation. The TT’s will be escalated every 30 mins if they are not
           acknowledged<o:p></o:p></span></span></span></li>
      </ol>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=350 valign=top style='width:262.2pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=1 type=a>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l4 level1 lfo6'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Get familiar with the “Slats”
           i.e. checks Palisade runs (</span></span></span><span style='mso-bookmark:
           _Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://w.amazon.com/bin/view/Palisade/Slats/"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>Palisade Slats</span></span></span><span style='mso-bookmark:
           _Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>) and avoid violating its checks.<o:p></o:p></span></span></span></li>
       <li class=MsoListParagraphCxSpLast style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l4 level1 lfo6'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Ensure you have </span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://w.amazon.com/bin/view/EnterpriseEngineering/SOS/Devices/Pong"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>Pong Paging</span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:EN-SG'>
           <span lang=EN-SG>installed and enabled on your mobile device. If by
           mistake you violated a Palisade Slat, you can acknowledge the TT and
           prevent it from being escalated.<o:p></o:p></span></span></span></span></li>
      </ol>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
     <tr style='mso-yfti-irow:3;mso-yfti-lastrow:yes'>
      <td width=274 valign=top style='width:205.3pt;border:solid windowtext 1.0pt;
      border-top:none;padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=3 type=1>
       <li class=MsoListParagraphCxSpFirst style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l1 level1 lfo3'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://security-dashboard.aws.a2z.com/dashboards/permalink/patching?filters=complianceFilter%3Bfalse%5EextensionStatusFilter%3Btrue%5EextensionsFilter%3B%7B%22label%22%3A%22all%20hosts%22%2C%22filterValue%22%3A%22A%22%7D%5EquiltFilter%3B%7B%22label%22%3A%22all%22%2C%22filterValue%22%3A%22A%22%7D%5EselectedHostFilters%3B%5B%7B%22label%22%3A%22NAWS%22%2C%22filterValue%22%3A%22NAWS%22%7D%2C%7B%22label%22%3A%22EC2FIXED%22%2C%22filterValue%22%3A%22EC2FIXED%22%7D%2C%7B%22label%22%3A%22EDGE%22%2C%22filterValue%22%3A%22EDGE%22%7D%2C%7B%22label%22%3A%22PROD%22%2C%22filterValue%22%3A%22AMZN%22%7D%2C%7B%22label%22%3A%22ACC%22%2C%22filterValue%22%3A%22ACC%22%7D%2C%7B%22label%22%3A%22HUMBOLDT%22%2C%22filterValue%22%3A%22HUMBOLDT%22%7D%2C%7B%22label%22%3A%22EC2BF%22%2C%22filterValue%22%3A%22EC2BF%22%7D%2C%7B%22label%22%3A%22CORP%22%2C%22filterValue%22%3A%22CORP%22%7D%5D%5EselectedInstanceStateFilter%3B%7B%22label%22%3A%22active%20instances%22%2C%22filterValue%22%3A%22A%22%7D%5E"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>Security Dashboard</span></span></span><span style='mso-bookmark:
           _Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><b><span
           style='mso-fareast-font-family:"Times New Roman"'> </span></b></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>for </span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://w.amazon.com/bin/view/AWS/VM/NAWS/"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>NAWS</span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           style='mso-fareast-font-family:"Times New Roman"'> </span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>Reporting and Patching: a tool called PVRE checks if EC2
           instances (including those spun up by managed services) are reporting
           software versions and are being patched for latest software versions,
           via SSM. While this feeds into Policy Engine, you can’t wait a week to
           acknowledge issues.<o:p></o:p></span></span></span></li>
      </ol>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
      <td width=350 valign=top style='width:262.2pt;border-top:none;border-left:
      none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
      padding:0cm 5.4pt 0cm 5.4pt'>
      <ol style='margin-top:0cm' start=1 type=a>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l6 level1 lfo7'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>Follow the Reporting and
           Patching guidance on the NAWS page for your EC2 instances.<o:p></o:p></span></span></span></li>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l6 level1 lfo7'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>When you create new instances
           directly or via managed services, you should check the </span></span></span><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span><a
           href="https://security-dashboard.aws.a2z.com/dashboards/permalink/patching?filters=complianceFilter;false%5EextensionStatusFilter;true%5EextensionsFilter;%7B%22label%22:%22all%20hosts%22,%22filterValue%22:%22A%22%7D%5EquiltFilter;%7B%22label%22:%22all%22,%22filterValue%22:%22A%22%7D%5EselectedHostFilters;%5B%7B%22label%22:%22NAWS%22,%22filterValue%22:%22NAWS%22%7D,%7B%22label%22:%22EC2FIXED%22,%22filterValue%22:%22EC2FIXED%22%7D,%7B%22label%22:%22EDGE%22,%22filterValue%22:%22EDGE%22%7D,%7B%22label%22:%22PROD%22,%22filterValue%22:%22AMZN%22%7D,%7B%22label%22:%22ACC%22,%22filterValue%22:%22ACC%22%7D,%7B%22label%22:%22HUMBOLDT%22,%22filterValue%22:%22HUMBOLDT%22%7D,%7B%22label%22:%22EC2BF%22,%22filterValue%22:%22EC2BF%22%7D,%7B%22label%22:%22CORP%22,%22filterValue%22:%22CORP%22%7D%5D%5EselectedInstanceStateFilter;%7B%22label%22:%22active%20instances%22,%22filterValue%22:%22A%22%7D%5E&amp;goal=reporting"><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'>dashboard</span></span></span><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'></span></span></a><span
           style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
           lang=EN-SG style='mso-fareast-font-family:"Times New Roman";mso-ansi-language:
           EN-SG'> here and check both the Reporting and Patching tabs to see if
           you have instances with issues.<o:p></o:p></span></span></span></li>
       <li class=MsoListParagraphCxSpMiddle style='margin-bottom:0cm;margin-left:
           -18.0pt;margin-bottom:.0001pt;mso-add-space:auto;line-height:normal;
           mso-list:l6 level1 lfo7'><span style='mso-bookmark:_Hlk76048917'><span
           style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-fareast-font-family:
           "Times New Roman";mso-ansi-language:EN-SG'>PVRE gets informed about new
           hosts and host state changes (stopped, started) once an hour (but this
           is not reflected immediately in the Security Dashboard).<o:p></o:p></span></span></span></li>
      </ol>
      <p class=MsoListParagraphCxSpMiddle style='margin-top:0cm;margin-right:0cm;
      margin-bottom:0cm;margin-left:54.0pt;margin-bottom:.0001pt;mso-add-space:
      auto;text-indent:-54.0pt;mso-text-indent-alt:-9.0pt;line-height:normal;
      mso-list:l3 level3 lfo8'><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><![if !supportLists]><span lang=EN-SG
      style='mso-fareast-font-family:Calibri;mso-ansi-language:EN-SG'><span
      style='mso-list:Ignore'><span style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      </span>i.<span style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      </span></span></span><![endif]><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>SSM sends a check-in the first time 5 mins after EC2 launch. Then it
      sends a check-in every 12 hours. This means updated software versions won’t
      be <b>reported </b>for up to 12 hours.<o:p></o:p></span></span></span></p>
      <p class=MsoListParagraphCxSpLast style='margin-top:0cm;margin-right:0cm;
      margin-bottom:0cm;margin-left:54.0pt;margin-bottom:.0001pt;mso-add-space:
      auto;text-indent:-54.0pt;mso-text-indent-alt:-9.0pt;line-height:normal;
      mso-list:l3 level3 lfo8'><span style='mso-bookmark:_Hlk76048917'><span
      style='mso-bookmark:_Hlk76117587'><![if !supportLists]><span lang=EN-SG
      style='mso-fareast-font-family:Calibri;mso-ansi-language:EN-SG'><span
      style='mso-list:Ignore'><span style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      </span>ii.<span style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      </span></span></span><![endif]><span lang=EN-SG style='mso-ansi-language:
      EN-SG'>PVRE generates static files once a day that then update Security
      Dashboard. This seems to happen between 7.30PM—1.30PM SGT.<o:p></o:p></spyle='tab-interval:36.0pt'>

    <div class=WordSection1>

    <p class=MsoNormal style='margin-left:165.0pt;text-indent:-165.0pt;tab-stops:
    165.0pt;mso-layout-grid-align:none;text-autospace:none'><b><span
    style='color:black'>From:<span style='mso-tab-count:1'>                                                       </span></span></b><span
    style='color:black'>Chia, Shana<o:p></o:p></span></p>

    <p class=MsoNormal style='margin-left:165.0pt;text-indent:-165.0pt;tab-stops:
    165.0pt;mso-layout-grid-align:none;text-autospace:none'><b><spaan></span></span></p>
      </td>
      <span style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'></span></span>
     </tr>
    </table>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
    EN-SG'><o:p>&nbsp;</o:p></span></span></span></p>

    <p class=MsoNormal><span style='mso-bookmark:_Hlk76048917'><span
    style='mso-bookmark:_Hlk76117587'><span lang=EN-SG style='mso-ansi-language:
    EN-SG'>We appreciate you taking the time and effort and keep security high! </span></span></span><span
    style='mso-bookmark:_Hlk76048917'><span style='mso-bookmark:_Hlk76117587'><span
    style='font-family:"Segoe UI Emoji",sans-serif;mso-bidi-font-family:"Segoe UI Emoji"'>&#128522;</span></span></span><span
    style='mso-bookmark:_Hlk76117587'></span><span style='mso-bookmark:_Hlk76048917'></span><span
    lang=EN-SG style='mso-ansi-language:EN-SG'><o:p></o:p></span></p>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    <p class=MsoNormal><span lang=EN-SG style='font-size:9.0pt;mso-ansi-language:
    EN-SG'>Warm regards,<o:p></o:p></span></p>

    <p class=MsoNormal><b><span lang=EN-SG style='font-size:9.0pt;color:#18376A;
    mso-ansi-language:EN-SG'>Shana Chia | Program Manager Intern, SA Team | AWS</span></b><span
    lang=EN-SG style='color:black;mso-ansi-language:EN-SG'><o:p></o:p></span></p>

    <p class=MsoNormal><span lang=EN-SG style='font-size:9.0pt;color:black;
    mso-ansi-language:EN-SG'>P: +65 86875242 &nbsp;| E: <a
    href="mailto:scchia@amazon.com">scchia@amazon.com</a><o:p></o:p></span></p>

    <p class=MsoNormal><span lang=EN-SG style='font-size:10.0pt;color:black;
    mso-ansi-language:EN-SG'>&nbsp;</span><span lang=EN-SG style='color:black;
    mso-ansi-language:EN-SG'><o:p></o:p></span></p>

    <p class=MsoNormal><span lang=EN-SG style='color:#18376A;mso-ansi-language:
    EN-SG'>

    ![if !vml]><img border=0 width=71 height=42
    src="ACTION%20REQUIRED%20Resolve%20Security%20Violations_files/image004.gif"
    style='height:.437in;width:.743in' alt="signature_1270978388" v:shapes="Picture_x0020_6"><![endif]></span><span
    lang=EN-SG style='color:black;mso-ansi-language:EN-SG'><o:p></o:p></span></p>

    <p class=MsoNormal><o:p>&nbsp;</o:p></p>

    </div>

    </body>

    </html>
                """         
    
    BODY_HTML = BODY_HTML_PRE.format(NUM_VIOLATE_1=NUM_VIOLATE_1,name=NAME,NUM_VIOLATE_2=NUM_VIOLATE_2,NUM_VIOLATE_3 = NUM_VIOLATE_3, DATE=DATE)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
    #         ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent to ",RECIPIENT," at ",DATE)
        print("Email sent! Message ID:"),
        print(response['MessageId'])

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
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket, Key=key)
            data = response["Body"].read()
            sheet_1 = pd.read_excel(io.BytesIO(data), sheet_name="mcnconor_2021-06-29_reporting_")
            sheet_2 = pd.read_excel(io.BytesIO(data), sheet_name="mcnconor_2021-06-29_patching_")
            sheet_3 = pd.read_excel(io.BytesIO(data), sheet_name="mcnconor_2021-06-29_policy_")

            sheet_1=sheet_1[['primary_owner','status']]
            sheet_1 = sheet_1[sheet_1['status'].notna()]
            sheet_1 = sheet_1[sheet_1.status != "GREEN"]
            sheet_1_count=sheet_1.groupby(['primary_owner']).count()

            sheet_2 = sheet_2[['primary_owner','status']]
            sheet_2 = sheet_2[sheet_2['status'].notna()]
            sheet_2 = sheet_2[sheet_2.status != "GREEN"]
            sheet_2_count=sheet_2.groupby(['primary_owner']).count()

            sheet_3=sheet_3[['Owner','Acked']]
            sheet_3 = sheet_3[sheet_3.Acked == "NO"]
            sheet_3_count=sheet_3.groupby(['Owner']).count()

            HR_dict = {} 
            for i in sheet_1_count.index:
                HR_dict[i] = [sheet_1_count['status'][i], 0, 0]
                
            for i in sheet_2_count.index:
                if i in HR_dict:
                    HR_dict[i] = [HR_dict[i][0], sheet_2_count['status'][i], HR_dict[i][2]]
                else:
                    HR_dict[i] = [0, sheet_2_count['status'][i], 0]
                
            for i in sheet_3_count.index:
                if i in HR_dict:
                    HR_dict[i] = [HR_dict[i][0], HR_dict[i][1], sheet_3_count['Acked'][i]]
                else:
                    HR_dict[i] = [0,  0, sheet_3_count['Acked'][i]]

            print(HR_dict)

            mock_dict = {'scchia':[1,4,5], 'thaiwg':[4,3,1]}

            for person in mock_dict:
                receipient_email = str(person)+"@amazon.com"
                name = str(person)
                num_1 = mock_dict[person][0]
                num_2 = mock_dict[person][1]
                num_3 = mock_dict[person][2]
                send_email(receipient_email, name, num_1, num_2, num_3)


