# a function that sends an email
def send_mail(reciever, carts):

    from email.mime.text import MIMEText
    import smtplib
    from dotenv import load_dotenv
    import os

    load_dotenv("credentials.env")
    from_address = os.getenv("from_address")
    password = os.getenv("password")

    def format_carts(carts):
        html = ""
        for shop, df in carts.items():
            html += f"<h3>{shop}</h3>"
            table_html = df.to_html(index=False, border=1)
            table_html = table_html.replace(
                '<table border="1" class="dataframe">',
                '<table style="border-collapse: collapse; width: 100%;">'
            )
            html += table_html
            html += "<br>"
        return html

    # Creating the body of message
    body = f"""
    <html>
    <body>
    <p>Dear {reciever},</p>

    <p>Here is your grocery list:</p>

    {format_carts(carts)}

    </body>
    </html>
    """

    msg = MIMEText(body, "html", "utf-8")
    msg['Subject'] = "Your Grocery list"
    msg["From"] = from_address
    msg["To"] = reciever

    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.starttls()
    smtp_object.login(from_address, password)

    smtp_object.sendmail(from_address, reciever, msg.as_string())
    smtp_object.quit()