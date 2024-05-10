from email.message import EmailMessage
import smtplib
import datetime
import dd_content
import os
from dotenv import load_dotenv

load_dotenv()


class DailyDigestEmail:
    def __init__(self):
        self.content = {
            "quote": {"include": True, "content": dd_content.get_random_quote()},
            "weather": {"include": True, "content": dd_content.get_weather()},
            "article": {"include": True, "content": dd_content.get_random_article()},
        }

        self.recipients_list = [
            "nicholas.callaghan@gmail.com",
            "nicholas.callaghan+label@gmail.com",
        ]

        self.sender_credentials = {
            "email": os.getenv("SMTP_EMAIL"),
            "password": os.getenv("SMTP_PASSWORD"),
        }

        self.message_text = ""
        self.message_html = ""

        self.format_message()

    def __str__(self):
        return f"""
        Email to: {", ".join(self.recipients_list)}\n
        From: {self.sender_credentials['email']}\n
        Message: {self.message_text}"""

    def format_message(self):
        # Format plain text messge
        self.message_text += f"""
        ~~~~~ Daily Digest for {datetime.datetime.today().strftime("%Y-%m-%d")} ~~~~~

        {self.content["quote"]["content"]["quote"]} - {self.content["quote"]["content"]["author"]}

        Weather for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]}:
        """

        for period in self.content["weather"]["content"]["periods"]:
            self.message_text += f"""
            {period["timestamp"].strftime("%Y-%m-%d %H:%M:%S")} - {period["description"]} - {period["temp"]}°C
            """

        self.message_text += f"""
        Random Wikipedia Article:
        {self.content["article"]["content"]["title"]}\n
        {self.content["article"]["content"]["extract"]}
        """

        # Format HTML message
        self.message_html += f"""
        <h1>~~~~~ Daily Digest for {datetime.datetime.today().strftime("%Y-%m-%d")} ~~~~~</h1>

        <h2>{self.content["quote"]["content"]["quote"]} - {self.content["quote"]["content"]["author"]}</h2>

        <h2>Weather for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]}:</h2>

        <ul>
        """

        for period in self.content["weather"]["content"]["periods"]:
            self.message_html += f"""
            <li>{period["timestamp"].strftime("%Y-%m-%d %H:%M:%S")} - {period["description"]} - {period["temp"]}°C</li>
            """

        self.message_html += f"""
        </ul>

        <h2>Random Wikipedia Article:</h2>
        <h3>{self.content["article"]["content"]["title"]}</h3>
        <p>{self.content["article"]["content"]["extract"]}</p>
        """

    def send_email(self):
        # Create message
        msg = EmailMessage()
        msg["Subject"] = (
            f"Daily Digest for {datetime.datetime.today().strftime('%Y-%m-%d')}"
        )
        msg["From"] = self.sender_credentials["email"]
        msg["To"] = ", ".join(self.recipients_list)

        # add plain text message and html content
        msg.set_content(self.message_text)
        msg.add_alternative(self.message_html, subtype="html")

        # Secure connection and send email
        try:
            print("Sending email...")
            with smtplib.SMTP(
                os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")
            ) as server:
                server.starttls()
                server.login(
                    self.sender_credentials["email"],
                    self.sender_credentials["password"],
                )
                server.send_message(msg)

        except Exception as e:
            print("Something went wrong:", e)


if __name__ == "__main__":
    email = DailyDigestEmail()
    email.send_email()
    print(f"Send email f{email}")
