from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

now = datetime.now()
previous_day = now - timedelta(days=1)
formatted_date = str(previous_day.strftime("%d-%B-%Y"))

url = f"https://www.skysports.com/football/fixtures-results/{formatted_date}"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')

team_elements = soup.find_all('span', class_ = "swap-text__target")
score_elements = soup.find_all('span', class_="matches__teamscores-side")

score_titles = [score.text.strip() for score in score_elements]
team_names = []

for team in team_elements:
    if(team.text.strip() != "Football"):
        team_names.append(team.text.strip())

count_teams = 0
count_scores = 0
full_results = []

while(count_teams < len(team_names) - 1):
    full_results.append(f"<li>{team_names[count_teams]} {score_titles[count_scores]} - {score_titles[count_scores + 1]} {team_names[count_teams + 1]}</li>")
    count_teams = count_teams + 2
    count_scores = count_scores + 2

subject = formatted_date + ": Football Scores"
result_string = "<ul>" + "".join(full_results) + "</ul>"
body = "Hi there!\nYesterday's football results:\n" + result_string

body_html = f"""
<html>
    <body>
        <h2>Hi there! </h2>
        <h3>Here are yesterday's football results:</h3>

        {result_string}
    </body>
</html>
"""

sender = "your_email@gmail.com"
recipients = ["recipient1@gmail.com", "recipient2@gmail.com"]
password_email = "your gmail app password"

def send_email(subject, body, sender, recipients, password_email):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password_email)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

send_email(subject, body_html, sender, recipients, password_email)

