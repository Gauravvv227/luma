import json

from groq import Groq
import os
from dotenv import load_dotenv

from tmdb import get_movie_details

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_recommendations(profile, notes_sample):
    genre_summary = ", ".join([
        f"{row['genre']} (avg rating: {row['avg_rating']}, {row['count']} entries)"
        for row in profile['avg_by_genre']
    ])
    
    type_summary = ", ".join([
        f"{row['type']}: {row['count']} entries"
        for row in profile['type_split']
    ])

    notes_text = "\n".join([
        f"- {row['title']} ({row['type']}, {row['genre']}, {row['rating']}/10): {row['notes']}"
        for row in notes_sample
    ])

    prompt =f"""You are a personal entertainment advisor. Based on this person's taste profile, recommend 3 movies and 3 songs.

TASTE PROFILE:
- What they consume: {type_summary}
- Genre preferences: {genre_summary}
- What they've said about their favorites:
{notes_text}

Respond ONLY with a JSON object, no extra text, no markdown, no backticks. Exactly this format:
{{
  "movies": ["Movie Title 1", "Movie Title 2", "Movie Title 3"],
  "songs": ["Song Title 1", "Song Title 2", "Song Title 3"]
}}"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    

    raw = response.choices[0].message.content
    print("RAW RESPONSE:", raw)

# Extract JSON from anywhere in the response
    import re
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not json_match:
        raise ValueError("No JSON found in response")

    clean = json_match.group(0)
    titles = json.loads(clean)
    

# Enrich movies with TMDB data
    movies = []
    for title in titles['movies']:
        details = get_movie_details(title)
    if details:
        movies.append(details)

    return {
    'movies': movies,
    'songs': titles['songs']
}