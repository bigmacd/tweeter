import email
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

from parseEmailSections import parseSections
from twitterPost import TwitterPoster

def read_eml_file(file_path: str):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Parse the email using the default policy
            msg = email.message_from_file(file, policy=policy.default)
            return msg
    except UnicodeDecodeError:
        # If UTF-8 fails, try with different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            msg = email.message_from_file(file, policy=policy.default)
            return msg


def extract_email_info(msg) -> dict:

    info = {
        'subject': msg.get('Subject', 'No Subject'),
        'from': msg.get('From', 'Unknown Sender'),
        'to': msg.get('To', 'Unknown Recipient'),
        'date': msg.get('Date', 'Unknown Date'),
        'cc': msg.get('Cc', ''),
        'bcc': msg.get('Bcc', ''),
        'body': '',
        'html_body': '',
        'attachments': []
    }
    
    # Extract body content
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Extract text body
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True)
                if body:
                    info['body'] = body.decode('utf-8', errors='ignore')
            
            # Extract HTML body
            elif content_type == "text/html" and "attachment" not in content_disposition:
                html_body = part.get_payload(decode=True)
                if html_body:
                    info['html_body'] = html_body.decode('utf-8', errors='ignore')
            
            # Extract attachments
            elif "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    info['attachments'].append({
                        'filename': filename,
                        'content_type': content_type,
                        'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                    })
    else:
        # Single part message
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            body = msg.get_payload(decode=True)
            if body:
                info['body'] = body.decode('utf-8', errors='ignore')
        elif content_type == "text/html":
            html_body = msg.get_payload(decode=True)
            if html_body:
                info['html_body'] = html_body.decode('utf-8', errors='ignore')
    
    return info

def moveLatestEmlFile() -> None:
    # Get a list of all .eml files in the current directory
    eml_files = [f for f in os.listdir('c:\\Users\\marti\\Downloads') if f.endswith('.eml')]
    
    if not eml_files:
        raise FileNotFoundError("No .eml files found in the current directory.")
    
    # Find the most recently modified .eml file
    os.rename(f"c:\\Users\\marti\\Downloads\\{eml_files[0]}", "latest.eml")
    #latest_file = max(eml_files, key=os.path.getmtime)
    #return latest_file


def getEmailHtmlBody() -> str:
    # Replace with your .eml file path
    eml_file_path = "latest.eml"
    moveLatestEmlFile()
    
    try:
        # Read the .eml file
        email_message = read_eml_file(eml_file_path)
        
        # Extract email information
        email_info = extract_email_info(email_message)
     
    except FileNotFoundError:
        print(f"Error: File '{eml_file_path}' not found.")
    except Exception as e:
        print(f"Error reading .eml file: {str(e)}")

    os.remove(eml_file_path)
    return email_info['html_body']


