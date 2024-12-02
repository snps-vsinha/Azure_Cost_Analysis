def send_mail(image, body):  
    import subprocess  
    from email.mime.text import MIMEText  
    from email.mime.multipart import MIMEMultipart  
    from email.mime.image import MIMEImage  
  
    sender = "vsinha@synopsys.com"  
    receivers = ["kollir@synopsys.com","voru@synopsys.com","vsinha@synopsys.com"]  
    subject = f"{body} - Azure Cost Analysis"
  
    image_paths = image 
  
    msg = MIMEMultipart('related')  
    msg['From'] = sender  
    msg['To'] = ", ".join(receivers)  
    msg['Subject'] = subject  
  
    msg_alternative = MIMEMultipart('alternative')  
    msg.attach(msg_alternative)  
  
    html_content = f"""  
    <html>  
    <body>  
        <p>{body}</p>  
        <table style="border-collapse: collapse; width: 100%;">  
    """  
  
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
  
    msg_html = MIMEText(html_content, 'html')  
    msg_alternative.attach(msg_html)  
  
    for i, image_path in enumerate(image_paths):  
        with open(image_path, "rb") as attachment:  
            img = MIMEImage(attachment.read())  
            img.add_header('Content-ID', f'<image{i+1}>')  
            img.add_header('Content-Disposition', 'inline', filename=image_path)  
            msg.attach(img)  
  
    process = subprocess.Popen(['/usr/sbin/sendmail', '-t', '-oi'], stdin=subprocess.PIPE)  
    process.communicate(msg.as_bytes()) 
    print("Email sent successfully!") 

# send_mail("plots/SNPS-OpenAI-SCE-Platform.png","Trial")
