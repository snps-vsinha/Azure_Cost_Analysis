import subprocess  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.mime.image import MIMEImage  
  
# Define email sender and receiver  
sender = "vsinha@synopsys.com"  
receivers = ["kollir@synopsys.com","voru@synopsys.com"]  
subject = "Azure Cost Analysis"  
body = "The following are the daily usage cost analysis"  
  
# List of image file paths  
image_paths = [ 
    "plots/SNPS-OpenAI-SCE-Platform.png" 
]  
  
# Create the multipart message  
msg = MIMEMultipart('related')  
msg['From'] = sender  
msg['To'] = ", ".join(receivers)  
msg['Subject'] = subject  

# Create the alternative part for the HTML content  
msg_alternative = MIMEMultipart('alternative')  
msg.attach(msg_alternative)  
  
# Start the HTML content  
html_content = f"""  
<html>  
  <body>  
    <p>{body}</p>  
    <table style="border-collapse: collapse; width: 100%;">  
"""  
  
# Append image tags in a single column format (15x1)  
for i, image_path in enumerate(image_paths):  
    html_content += f'''  
    <tr>  
        <td style="border: 1px solid black; padding: 10px; text-align: center; vertical-align: middle;">  
            <img src="cid:image{i+1}" style="max-width: 100%; height: auto; display: block; margin: auto;">  
        </td>  
    </tr>  
    '''  
  
html_content += """  
    </table>  
  </body>  
</html>  
"""  
  
# Attach the HTML content  
msg_html = MIMEText(html_content, 'html')  
msg_alternative.attach(msg_html)  
  
# Attach the images  
for i, image_path in enumerate(image_paths):  
    with open(image_path, "rb") as attachment:  
        img = MIMEImage(attachment.read())  
        img.add_header('Content-ID', f'<image{i+1}>')  
        img.add_header('Content-Disposition', 'inline', filename=image_path)  
        msg.attach(img)  
  
# Send the email using subprocess and sendmail  
process = subprocess.Popen(['/usr/sbin/sendmail', '-t', '-oi'], stdin=subprocess.PIPE)  
process.communicate(msg.as_bytes())  
  
print("Email sent successfully!")
