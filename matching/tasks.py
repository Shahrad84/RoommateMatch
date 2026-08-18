from celery import shared_task
import requests
import json
import os
from django.conf import settings
from accounts.models import Account
from profiles.models import Profile, LifestyleProfile, Preference


URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.environ.get('OPENROUTER_API_KEY', '')

@shared_task
def analyze_single_user_task(user_data, target_data):
    

    
    prompt = f"""
You are a roommate compatibility analyzer. Analyze compatibility between two users.

USER:
{json.dumps(user_data, indent=2)}

CANDIDATE:
{json.dumps(target_data, indent=2)}

Provide:
1. compatibility_score: 0-100
2. positive_points: 2-4 strings
3. concerns: 2-4 strings
4. summary: One sentence

Return ONLY valid JSON:
{{
    "user_id": {target_data['id']},
    "compatibility_score": 85,
    "positive_points": ["point1", "point2"],
    "concerns": ["concern1", "concern2"],
    "summary": "Overall assessment"
}}
"""
    
    try:
        response = requests.post(
            URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://127.0.0.1:8000",
                "X-Title": "RoommateMatch"
            },
            json={
                "model": "nvidia/nemotron-nano-9b-v2:free",
                "messages": [
                    {"role": "system", "content": "You are a roommate analyzer. Return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            content = content.replace('```json', '').replace('```', '').strip()
            return json.loads(content)
        else:
            print(f"API error for user {target_data['id']}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error analyzing user {target_data['id']}: {e}")
        return None


@shared_task
def analyze_matches_task(user_id, target_user_ids):
    """
    Main task: Analyze compatibility for multiple users in parallel.
    """

    
    user = Account.objects.get(id=user_id)
    user_profile = Profile.objects.get(account=user)
    user_lifestyle = LifestyleProfile.objects.get(account=user)
    user_preference = Preference.objects.get(account=user)
    
    user_data = {
        "username": user.username,
        "age": user.age,
        "job": user_profile.job,
        "lifestyle": {
            "cleanliness": user_lifestyle.cleanliness,
            "noise": user_lifestyle.noise_generating,
            "social": user_lifestyle.social_activity,
            "sleep": str(user_lifestyle.sleep),
            "smoking": user_lifestyle.smoking,
            "has_pets": user_lifestyle.has_pets,
        },
        "preferences": {
            "cleanliness_importance": user_preference.cleanliness_importance,
            "max_noise": user_preference.max_noise,
        }
    }
    
    # Create parallel tasks for each target
    parallel_tasks = []
    
    for target_id in target_user_ids:
        try:
            target = Account.objects.get(id=target_id)
            target_profile = Profile.objects.get(account=target)
            target_lifestyle = LifestyleProfile.objects.get(account=target)
            
            target_data = {
                "id": target.id,
                "username": target.username,
                "age": target.age,
                "job": target_profile.job,
                "lifestyle": {
                    "cleanliness": target_lifestyle.cleanliness,
                    "noise": target_lifestyle.noise_generating,
                    "social": target_lifestyle.social_activity,
                    "sleep": str(target_lifestyle.sleep),
                    "smoking": target_lifestyle.smoking,
                    "has_pets": target_lifestyle.has_pets,
                }
            }
            
            # Create async task for this user
            task = analyze_single_user_task.delay(user_data, target_data)
            parallel_tasks.append({
                'target_id': target_id,
                'task': task,
            })
            
        except (Account.DoesNotExist, Profile.DoesNotExist, LifestyleProfile.DoesNotExist):
            continue
    
    # Wait for all tasks to complete
    results = []
    
    for item in parallel_tasks:
        try:
            result = item['task'].get(timeout=60)
            if result:
                results.append(result)
        except Exception as e:
            print(f"Task failed for user {item['target_id']}: {e}")
    
    # Sort by score
    #results.sort(key=lambda x: x.get('compatibility_score', 0), reverse=True)
    
    return results