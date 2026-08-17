from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from profiles.models import Profile, LifestyleProfile, Preference
import random
import requests
import json
from django.conf import settings
import os


URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-nano-9b-v2:free"


@login_required(login_url='/accounts/login/')
@login_required(login_url='/accounts/login/')
def explore(request):
    user = request.user
    
    user_city = user.city
    
    try:
        user_lifestyle = LifestyleProfile.objects.get(account=user)
        user_preference = Preference.objects.get(account=user)
    except (LifestyleProfile.DoesNotExist, Preference.DoesNotExist):
        return render(request, 'templates/explore.html', {
            'error': 'Please complete your profile first.',
            'candidates': []
        })
    
    same_city_users = Account.objects.filter(city=user_city).exclude(id=user.id)
    
    # Randomly select up to 20 users
    user_ids = list(same_city_users.values_list('id', flat=True))
    
    if len(user_ids) > 20:
        selected_ids = random.sample(user_ids, 20)
    else:
        selected_ids = user_ids
    
    candidates = []
    
    for target_id in selected_ids:
        try:
            target_account = Account.objects.get(id=target_id)
            target_lifestyle = LifestyleProfile.objects.get(account=target_account)
            target_preference = Preference.objects.get(account=target_account)
            
            candidates.append({
                'account': target_account,
                'lifestyle': target_lifestyle,
                'preference': target_preference,
            })
        except (LifestyleProfile.DoesNotExist, Preference.DoesNotExist):
            continue
    
    # Hard Filters
    accepted = []
    rejected = []
    
    for candidate in candidates:
        passed = True
        reject_reason = ""
        
        # Pets filter
        if user_preference.accepts_pets == False and candidate['lifestyle'].has_pets == True:
            passed = False
            reject_reason = "Has pets"
        
        # Smoking filter
        if passed and user_preference.accepts_smoking == False and candidate['lifestyle'].smoking == True:
            passed = False
            reject_reason = "Smokes"
        
        # Noise filter
        if passed and user_preference.max_noise <= 3 and candidate['lifestyle'].noise_generating >= 8:
            passed = False
            reject_reason = "Too noisy"
        
        # Sleep schedule filter
        if passed and user_preference.sleep_schedule_importance >= 8:
            sleep_diff = abs(user_lifestyle.sleep.hour - candidate['lifestyle'].sleep.hour)
            if sleep_diff >= 4:
                passed = False
                reject_reason = "Sleep schedule too different"
        
        if passed:
            accepted.append(candidate)
        else:
            rejected.append({
                'username': candidate['account'].username,
                'reason': reject_reason,
            })
    
    # Print hard filter results
    print("\n" + "="*50)
    print(f"🔍 EXPLORE RESULTS FOR {user.username}")
    print("="*50)
    print(f"Total digged: {len(candidates)}")
    print(f"Accepted: {len(accepted)}")
    print(f"Rejected: {len(rejected)}")
    print("\n--- REJECTED ---")
    for r in rejected:
        print(f"  ❌ {r['username']}: {r['reason']}")
    print("\n--- ACCEPTED ---")
    for c in accepted:
        lifestyle = c['lifestyle']
        print(f"  ✅ {c['account'].username} | Job: {c['account'].profile.job if hasattr(c['account'], 'profile') else 'N/A'} | Clean: {lifestyle.cleanliness}/10 | Noise: {lifestyle.noise_generating}/10 | Social: {lifestyle.social_activity}/10")
    print("="*50 + "\n")
    
    # ========================================
    # AI ANALYSIS SECTION - PUT THE CODE HERE
    # ========================================
    
    if accepted:
        target_accounts = [c['account'] for c in accepted]
        ai_results = analyse_with_ai(user, target_accounts)
        
        # Add AI analysis to accepted candidates
        for candidate in accepted:
            candidate_id = candidate['account'].id
            for ai_result in ai_results:
                if ai_result.get('user_id') == candidate_id:
                    candidate['analysis'] = ai_result
                    break
        
        # Print AI results to terminal
        print("\n" + "="*60)
        print(f"🤖 AI ANALYSIS RESULTS")
        print("="*60)
        
        for ai_result in ai_results:
            print(f"\n👤 User ID: {ai_result.get('user_id')}")
            print(f"   Score: {ai_result.get('compatibility_score')}/100")
            print(f"   Summary: {ai_result.get('summary')}")
            print(f"   ✅ Positive Points:")
            for point in ai_result.get('positive_points', []):
                print(f"      - {point}")
            print(f"   ⚠️ Concerns:")
            for concern in ai_result.get('concerns', []):
                print(f"      - {concern}")
            print("-"*60)
        
        print("="*60 + "\n")
    
    return render(request, 'templates/explore.html', {
        'candidates': accepted,
        'rejected': rejected,
        'total_digged': len(candidates),
        'total_accepted': len(accepted),
        'total_rejected': len(rejected),
    })


def analyse_with_ai(user, target_users):
    """
    Send user + target users to AI for compatibility analysis.
    Returns list of dicts with analysis results, or empty list if AI fails.
    """
    
    # Step 1: Get user's data
    user_profile = Profile.objects.get(account=user)
    user_lifestyle = LifestyleProfile.objects.get(account=user)
    user_preference = Preference.objects.get(account=user)
    
    # Step 2: Prepare user data for AI
    user_data = {
        "username": user.username,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "city": user.city.name if user.city else "Not set",
        "job": user_profile.job,
        "bio": user_profile.bio,
        "lifestyle": {
            "smoking": user_lifestyle.smoking,
            "cleanliness": user_lifestyle.cleanliness,
            "noise_generating": user_lifestyle.noise_generating,
            "social_activity": user_lifestyle.social_activity,
            "wake_up": str(user_lifestyle.wake_up),
            "sleep": str(user_lifestyle.sleep),
            "has_pets": user_lifestyle.has_pets,
            "guests_frequency": user_lifestyle.guests_frequency,
            "cooking": user_lifestyle.cooking,
        },
        "preferences": {
            "cleanliness_importance": user_preference.cleanliness_importance,
            "noise_importance": user_preference.noise_importance,
            "max_noise": user_preference.max_noise,
            "social_importance": user_preference.social_importance,
            "preferred_social_activity": user_preference.preferred_social_activity,
            "sleep_schedule_importance": user_preference.sleep_schedule_importance,
            "guests_importance": user_preference.guests_importance,
            "max_guests_frequency": user_preference.max_guests_frequency,
            "cooking_importance": user_preference.cooking_importance,
            "accepts_pets": user_preference.accepts_pets,
            "accepts_smoking": user_preference.accepts_smoking,
        }
    }
    
    # Step 3: Prepare target users data
    targets_data = []
    
    for target in target_users:
        try:
            target_profile = Profile.objects.get(account=target)
            target_lifestyle = LifestyleProfile.objects.get(account=target)
            
            targets_data.append({
                "id": target.id,
                "username": target.username,
                "name": target.name,
                "age": target.age,
                "gender": target.gender,
                "job": target_profile.job,
                "bio": target_profile.bio,
                "lifestyle": {
                    "smoking": target_lifestyle.smoking,
                    "cleanliness": target_lifestyle.cleanliness,
                    "noise_generating": target_lifestyle.noise_generating,
                    "social_activity": target_lifestyle.social_activity,
                    "wake_up": str(target_lifestyle.wake_up),
                    "sleep": str(target_lifestyle.sleep),
                    "has_pets": target_lifestyle.has_pets,
                    "guests_frequency": target_lifestyle.guests_frequency,
                    "cooking": target_lifestyle.cooking,
                },
            })
        except (Profile.DoesNotExist, LifestyleProfile.DoesNotExist):
            continue
    
    if not targets_data:
        return []
    
    # Step 4: Build prompt for AI
    prompt = f"""
    You are a roommate compatibility analyzer. Analyze the compatibility between a user and multiple potential roommates.

    USER PROFILE:
    {json.dumps(user_data, indent=2)}

    POTENTIAL ROOMMATES:
    {json.dumps(targets_data, indent=2)}

    For EACH potential roommate, provide:
    1. compatibility_score: A number from 0-100 indicating overall match
    2. positive_points: List of 2-4 strings describing what makes them compatible
    3. concerns: List of 2-4 strings describing potential problems
    4. summary: One sentence overall assessment

    Consider:
    - Cleanliness habits and importance
    - Noise levels and tolerance
    - Social activity preferences
    - Sleep schedules
    - Smoking and pets preferences
    - Guests frequency
    - Cooking habits

    Return ONLY valid JSON in this exact format:
    [
        {{
            "user_id": 1,
            "compatibility_score": 85,
            "positive_points": ["Both value cleanliness", "Similar sleep schedules"],
            "concerns": ["Different social energy levels"],
            "summary": "Great match overall with minor social differences."
        }}
    ]
    """
    
    ai_response = call_ai_api(prompt)
    
    if ai_response is None:
        print("⚠️ AI API unavailable. Skipping analysis.")
        return []
    
    ai_response = ai_response.replace('```json', '').replace('```', '').strip()
    
    # Parse JSON
    try:
        analysis_results = json.loads(ai_response)
        print(f"✅ AI analysis complete for {len(analysis_results)} users")
        return analysis_results
    except json.JSONDecodeError:
        print("⚠️ Failed to parse AI response. Skipping analysis.")
        return []


def call_ai_api(prompt):
    
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
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a roommate compatibility analyzer. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"❌ API Error ({response.status_code}): {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


