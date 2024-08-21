import random
from credentials import *
from email.message import EmailMessage
import smtplib

def sendVerificationOTP(email):
    otp = str(random.randint(1000, 9999))
    msg = EmailMessage()
    msg['Subject'] = 'Your EssayGrader Verification OTP'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    heading = '''
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style type="text/css">
                h1{font-size:56px}
                h2{font-size:28px;font-weight:900}
                p{font-weight:100}
                td{vertical-align:top}
                #email{margin:auto;width:600px;background-color:#fff}
                </style>
            </head>
            '''

    msg.set_content(heading + f'''
            <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
            <div id="email">
                <table role="presentation" width="100%">
                    <tr>
                        <td bgcolor="dodgerblue" align="center" style="color: white;">
                            <h1>Advanced Login</h1>
                        </td>
                </table>
                <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                    <tr>
                        <td>
                            <h3>Your EssayGrader OTP is {otp}</h3>
                            <p>Please Dont give this OTP if you didn't sign for this service</p>
                        </td>
                    </tr>
                </table>
            </div>
            </body>
            </html>''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return otp