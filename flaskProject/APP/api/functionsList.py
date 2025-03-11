import json
import pandas as pd
from io import StringIO
import imaplib
import email
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header



def calculate_total_age_function(input_json):
    """
    Calculate the total age from a JSON string in 'split' orientation.
    """
    df = pd.read_json(StringIO(input_json), orient='split')
    print(df)
    total_age = df['Age'].sum()
    return json.dumps({"total_age": str(total_age)})


def calculate_married_count_function(input_json):
    """
    Calculate the count of married individuals from a JSON string in 'split' orientation.
    """
    df = pd.read_json(StringIO(input_json), orient='split')
    married_count = df[df['IsMarried'] == True].shape[0]
    return json.dumps({"married_count": str(married_count)})


def fetch_last_email(user_email: str, user_pass: str) -> str:
    """
    查询指定用户的QQ邮箱中最后一封邮件信息。

    参数:
    user_email (str): 需要查询的QQ邮箱的用户邮箱。
    user_pass (str): 需要查询的QQ邮箱的用户码。

    返回:
    str: 包含最后一封邮件全部信息的JSON格式字符串。如果查询失败，返回包含错误信息的JSON格式字符串。
    """
    try:
        print("00000000000000000000000000")
        # 连接到QQ邮箱的IMAP服务器
        mail = imaplib.IMAP4_SSL("imap.qq.com")
        # 登录到邮箱
        mail.login(user_email, user_pass)
        # 选择收件箱
        mail.select("inbox")
        # 搜索所有邮件
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return json.dumps({"error": "Failed to search emails."})
        # 获取最新邮件的ID
        messages = messages[0].split()
        if not messages:
            return json.dumps({"error": "No emails found."})
        latest_email_id = messages[-1]
        # 获取最新邮件
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        if status != "OK":
            return json.dumps({"error": "Failed to fetch email."})
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # 解析邮件
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                email_info = {
                    "subject": subject,
                    "from": from_,
                    "body": body,
                }
                return json.dumps(email_info)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        try:
            mail.logout()
        except:
            pass


def send_email(sender_email: str, sender_pass: str, recipient_email: str, subject: str, body: str) -> str:
    """
    使用QQ邮箱向指定的收件人发送邮件。

    参数:
    sender_email (str): 发件人的QQ邮箱地址。
    sender_pass (str): 发件人的QQ邮箱授权码。
    recipient_email (str): 收件人的邮箱地址。
    subject (str): 邮件主题。
    body (str): 邮件正文。

    返回:
    str: 邮件发送的结果信息。
    """
    try:
        # 创建一个多部分的邮件
        message = MIMEMultipart()
        message['From'] = Header(sender_email)
        message['To'] = Header(recipient_email)
        message['Subject'] = Header(subject)

        # 添加邮件正文
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # 调试信息
        print("Connecting to SMTP server...")

        # 连接到QQ邮箱的SMTP服务器
        smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 打开调试输出
        smtp_server.set_debuglevel(1)

        print("Logging in...")
        smtp_server.login(sender_email, sender_pass)
        print(f"sender_email:{sender_email}")
        print("Sending email...")
        smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        print("Quitting SMTP server...")
        smtp_server.quit()

        return json.dumps({"result": "Email sent successfully."})
    except Exception as e:
        return json.dumps({"error": str(e)})
