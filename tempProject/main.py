from uAgents import Agent,Context,Model
import requests

api_key="664cc478ad44c46adfbc4782b2e21473"
def get_current_temperature(location):
    base_url='https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={664cc478ad44c46adfbc4782b2e21473}'

class temperature_data(Model):
    temperature:float 

class temperature_alert_agent(Agent):
    def _init_(self,name,seed,api_key,location,email_config):
        super()._init_(name=name,seed=seed)
        self.api_key=api_key
        self.location=location
        self.email_config=email_config

    async def fetch_temperature(self):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={664cc478ad44c46adfbc4782b2e21473}"
            response = requests.get(url)
            data = response.json()
            temperature = data["main"]["temp"]
            return temperature
        except Exception as e:
            print(f"Error fetching temperature data: {e}")
            return None
    async def check_temperature(self, min_temp, max_temp):
        current_temp = await self.fetch_temperature()
        if current_temp is not None:
            if current_temp < min_temp:
                self.alert_user(f"Temperature Alert: It's too cold! Current temperature is {current_temp}°C.")
            elif current_temp > max_temp:
                self.alert_user(f"Temperature Alert: It's too hot! Current temperature is {current_temp}°C.")