import os
import requests
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ১. সিক্রেট এনভায়রনমেন্ট ভেরিয়েবল থেকে লিংক রিড করা
API_LIVE_EVENTS = os.getenv("API_LIVE_EVENTS")
API_TRENDING_PLAYERS = os.getenv("API_TRENDING_PLAYERS")
API_SCHEDULED = os.getenv("API_SCHEDULED")

def fetch_data(url):
    if not url:
        print("API URL পাওয়া যায়নি!")
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        print(f"Error Status Code: {response.status_code}")
    except Exception as e:
        print(f"API থেকে ডাটা আনতে সমস্যা হয়েছে: {e}")
    return None

def create_summary_image(live_count, player_name, updated_at):
    # ৬০০x৪০০ সাইজের ডার্ক ব্যাকগ্রাউন্ড কার্ড জেনারেট করা
    img = Image.new('RGB', (600, 400), color='#0f172a')
    draw = ImageDraw.Draw(img)
    
    # টাইটেল ও তথ্য আঁকা
    draw.rectangle([20, 20, 580, 380], outline='#84cc16', width=3)
    
    draw.text((40, 50), "FOOTBALL LIVE DASHBOARD", fill='#84cc16')
    draw.text((40, 120), f"Live Matches: {live_count}", fill='#ffffff')
    draw.text((40, 180), f"Top Trending Player: {player_name}", fill='#ffffff')
    draw.text((40, 300), f"Last Updated: {updated_at}", fill='#94a3b8')

    # জেনারেট হওয়া ইমেজ সেভ করা
    img.save("status_summary.png")
    print("নতুন ইমেজ জেনারেট হয়েছে: status_summary.png")

def main():
    print("অটোমেশন শুরু হচ্ছে...")
    
    # লাইভ ডাটা ও ট্রেন্ডিং প্লেয়ার সংগ্রহ
    live_data = fetch_data(API_LIVE_EVENTS)
    trending_data = fetch_data(API_TRENDING_PLAYERS)
    
    # প্রয়োজন অনুযায়ী ডাটা প্রসেসিং
    live_count = len(live_data.get('data', [])) if live_data and isinstance(live_data, dict) else 0
    
    player_name = "N/A"
    if trending_data and 'data' in trending_data and len(trending_data['data']) > 0:
        player_name = trending_data['data'][0].get('name', 'Unknown')
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ইমেজ তৈরি
    create_summary_image(live_count, player_name, current_time)
    
    # ডাটা ব্যাকআপ রাখার জন্য JSON সেভ (অপশনাল)
    output_summary = {
        "updated_at": current_time,
        "live_matches": live_count,
        "top_player": player_name
    }
    with open("data_summary.json", "w", encoding="utf-8") as f:
        json.dump(output_summary, f, indent=4)

if __name__ == "__main__":
    main()
