#!/usr/bin/env python3
"""
Script to generate djembe instructional images using DALL-E API
Usage: OPENAI_API_KEY=your_key_here python3 generate_images.py
"""

import os
import sys
import requests

def generate_image(api_key, prompt, filename):
    """Generate a single image using DALL-E API"""
    print(f"\nGenerating {filename}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "style": "natural"
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                media_dir = "media"
                os.makedirs(media_dir, exist_ok=True)
                filepath = os.path.join(media_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                print(f"✅ Successfully created {filename}")
                return True
            else:
                print(f"❌ Failed to download {filename}")
                return False
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("\nUsage: OPENAI_API_KEY=your_key_here python3 generate_images.py")
        sys.exit(1)
    
    print("🎨 Generating djembe instructional images in pencil sketch style...\n")
    
    # Define images to generate
    images = [
        (
            "image1.png",
            """Pencil sketch drawing showing a djembe drum positioned between a person's legs. 
            The drum is tilted at 30-45 degrees away from the player. 
            View from the side showing the drum placement. 
            Clean, educational illustration style with clear lines and shading.
            Simple, instructional drawing like from a music textbook.
            Black and white pencil drawing."""
        ),
        (
            "image2.png",
            """Pencil sketch drawing showing hands positioned on top of a djembe drum membrane.
            Hands are 15-20 cm apart from the sides of the drum.
            Palms at 90-degree angle to the drum surface.
            Forearms straight from fingertips to elbows.
            Top-down view focusing on hand placement.
            Clear, instructional drawing style with pencil shading.
            Black and white educational illustration."""
        ),
        (
            "image3.jpg",
            """Pencil sketch drawing showing full body posture of a person sitting and playing djembe.
            Person sitting on a chair with feet flat on floor, shoulder-width apart.
            Djembe drum between legs, tilted 30-45 degrees forward.
            Drum membrane at solar plexus level.
            Shoulders relaxed, arms in proper position.
            Side view showing proper seated posture.
            Educational textbook-style pencil illustration.
            Black and white drawing with careful shading."""
        )
    ]
    
    # Generate each image
    success_count = 0
    for filename, prompt in images:
        if generate_image(api_key, prompt, filename):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Successfully generated {success_count}/{len(images)} images")
    print(f"{'='*50}")
    
    if success_count == len(images):
        print("\n🎉 All images created successfully!")
        print("Images saved in: media/")
    else:
        print(f"\n⚠️  {len(images) - success_count} image(s) failed to generate")
        sys.exit(1)

if __name__ == "__main__":
    main()
