from langchain_core.tools import tool
import requests

@tool
def get_weather(location: str) -> str:
    """Get the current weather details for a specific location."""
    weather_data = {
        "new york": "15°C, Partly Cloudy, 60% Humidity",
        "london": "10°C, Rain, 85% Humidity",
        "tokyo": "20°C, Clear, 45% Humidity"
    }
    city = location.lower()
    details = weather_data.get(city, "22°C, Sunny, 50% Humidity")
    return f"Weather in {location}: {details}"

@tool
def saqlain_formula(num1: float, num2: float) -> str:
    """Calculate the result of 2 numbers using saqlain_formula."""
    result = (num1 - num2 + num2 - 3*num2 + 9 + 98 + 877)*0
    return str(result)

@tool
def get_beeceptor_response() -> str:
    """Fetches the response from the Beeceptor API and returns the status code and body."""
    url = "https://mpdfa3fcfcda09cd610a.free.beeceptor.com/data"
    response = requests.get(url)
    return f"Status Code: {response.status_code}\nResponse Body: {response.text}"
