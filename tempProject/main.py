from uAgents import Agent, Context, Model
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os


class Message(Model):
    temperature: float

def get_temperature(lat,lon):
    try:
        
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=664cc478ad44c46adfbc4782b2e21473"
        response = requests.get(api_url)
        data = response.json()
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15   
        return temperature_celsius
    except Exception as e:
        print(f"Error fetching temperature: {e}")
        return None


def send_email(subject, body):
    try:
       
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  
        smtp_username = "smtp.gmAail"
        smtp_password = "Lizard!156"
        sender_email = "techbeast1004@gmail.com"
        recipient_email = "yuvrajsrsingh@gmail.com"

        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)  

       
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

       
        message.attach(MIMEText(body, "plain"))

        
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

min_temperature = float(input("Enter the minimum temperature (in Celsius): "))
max_temperature = float(input("Enter the maximum temperature (in Celsius): "))
location = input("Enter the location for temperature alerts: ")


location = input("Enter the location (latitude,longitude) for temperature alerts (e.g., 40.7128,-74.0060): ")
lat, lon = location.split(',')  

agent = Agent(name="temperature_alert_agent")

@agent.on_interval(period=10)  
async def check_temperature(ctx: Context):
    temperature = get_temperature(lat, lon)
    if temperature is not None:
        if temperature < min_temperature:
            subject = "Temperature Alert: Below Minimum"
            body = f"The current temperature in the specified location is {temperature}°C, which is below the minimum limit of {min_temperature}°C."
            send_email(subject, body)
        elif temperature > max_temperature:
            subject = "Temperature Alert: Above Maximum"
            body = f"The current temperature in the specified location is {temperature}°C, which is above the maximum limit of {max_temperature}°C."
            send_email(subject, body)



if __name__ == "__main__":
    agent.run()