from django.http import HttpResponse
import random

jokes = [
    "Why don’t skeletons ever go trick or treating? Because they have no body to go with.",
    "Why did the computer go to the doctor? Because it caught a virus!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
]

quotes = [
    "The best way to get started is to quit talking and begin doing. – Walt Disney",
    "Don’t let yesterday take up too much of today. – Will Rogers",
    "It’s not whether you get knocked down, it’s whether you get up. – Vince Lombardi",
]

def home(request):
    joke = random.choice(jokes)
    quote = random.choice(quotes)
    html = f"""
        <h1>Hello World 👋</h1>
        <h2>Here’s a Joke 😂</h2>
        <p>{joke}</p>
        <h2>Inspirational Quote 💡</h2>
        <p>{quote}</p>
    """
    return HttpResponse(html)
