"""
AgriAI - Zero Capital Edition
A complete agricultural AI assistant that runs on $0/month

Stack:
- FastAPI (backend)
- Supabase (database)
- WhatsApp Business API (communication)
- Groq (free AI)
- Railway (hosting)
"""

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
import httpx
import json
from typing import Optional, Dict, List
from datetime import datetime
import asyncio
from supabase import create_client, Client
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

app = FastAPI(
    title="AgriAI - Zero Capital Edition",
    description="Free AI farming assistant via WhatsApp",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "your_verify_token_123")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Initialize Supabase client
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

async def get_user_by_phone(phone: str) -> Optional[Dict]:
    """Get user from database by phone number"""
    if not supabase:
        return None
    try:
        result = supabase.table("users").select("*").eq("phone", phone).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


async def create_user(phone: str, name: str = "Farmer") -> Dict:
    """Create new user in database"""
    if not supabase:
        return {"id": "temp", "phone": phone, "name": name}
    
    try:
        # Generate referral code
        referral_code = hashlib.md5(phone.encode()).hexdigest()[:8].upper()
        
        result = supabase.table("users").insert({
            "phone": phone,
            "name": name,
            "referral_code": referral_code,
            "referrals": 0,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"id": "temp", "phone": phone, "name": name}


async def save_diagnosis(user_id: str, diagnosis: Dict) -> bool:
    """Save diagnosis to database"""
    if not supabase:
        return False
    
    try:
        supabase.table("diagnoses").insert({
            "user_id": user_id,
            "crop": diagnosis.get("crop", "unknown"),
            "issue": diagnosis.get("issue", ""),
            "confidence": diagnosis.get("confidence", 0),
            "recommendation": diagnosis.get("recommendation", ""),
            "method": diagnosis.get("method", "unknown"),
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return True
    except Exception as e:
        print(f"Error saving diagnosis: {e}")
        return False


async def save_feedback(user_id: str, diagnosis_id: str, feedback_type: str, notes: str = "") -> bool:
    """Save user feedback for RLHF"""
    if not supabase:
        return False
    
    try:
        supabase.table("feedback").insert({
            "user_id": user_id,
            "diagnosis_id": diagnosis_id,
            "feedback_type": feedback_type,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False

# ============================================================================
# AI ENGINE
# ============================================================================

class FreeAIEngine:
    """
    AI engine using free APIs
    Falls back to rule-based system if APIs fail
    """
    
    def __init__(self):
        self.groq_api_key = GROQ_API_KEY
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
    
    async def diagnose_crop(
        self,
        crop: str,
        observations: str,
        location: str = "unknown",
        weather: Optional[Dict] = None
    ) -> Dict:
        """
        AI-powered crop diagnosis
        """
        # Try AI first
        if self.groq_api_key:
            try:
                ai_diagnosis = await self._call_groq_ai(crop, observations, location, weather)
                if ai_diagnosis:
                    return ai_diagnosis
            except Exception as e:
                print(f"AI diagnosis failed: {e}")
        
        # Fallback to rule-based
        return self._rule_based_diagnosis(crop, observations)
    
    async def _call_groq_ai(
        self,
        crop: str,
        observations: str,
        location: str,
        weather: Optional[Dict]
    ) -> Optional[Dict]:
        """Call Groq AI API (free tier)"""
        
        weather_info = ""
        if weather and "current_weather" in weather:
            cw = weather["current_weather"]
            weather_info = f"\nCurrent weather: {cw.get('temperature', 'N/A')}°C, Wind: {cw.get('windspeed', 'N/A')} km/h"
        
        prompt = f"""You are an expert agricultural advisor. Analyze this farmer's situation and provide actionable advice.

Crop: {crop}
Location: {location}
Farmer's observation: {observations}{weather_info}

Provide a diagnosis in this exact JSON format:
{{
    "crop": "{crop}",
    "issue": "brief description of the problem",
    "confidence": 75,
    "recommendation": "specific action to take",
    "risk": "low/medium/high",
    "method": "ai"
}}

Be specific and practical. Focus on low-cost solutions."""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.groq_url,
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "max_tokens": 500
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Try to extract JSON
                    start = content.find("{")
                    end = content.rfind("}") + 1
                    if start >= 0 and end > start:
                        diagnosis = json.loads(content[start:end])
                        return diagnosis
                
            except Exception as e:
                print(f"Groq API error: {e}")
        
        return None
    
    def _rule_based_diagnosis(self, crop: str, observations: str) -> Dict:
        """
        Simple rule-based diagnosis
        Works without any AI API
        """
        obs_lower = observations.lower()
        
        # Keyword matching for common issues
        if any(word in obs_lower for word in ["yellow", "yellowing", "pale"]):
            if "leaves" in obs_lower or "leaf" in obs_lower:
                return {
                    "crop": crop,
                    "issue": "Nitrogen deficiency (yellowing leaves)",
                    "confidence": 70,
                    "recommendation": "Apply urea fertilizer (50kg per hectare) or compost. Water regularly.",
                    "risk": "medium",
                    "method": "rule-based"
                }
        
        if any(word in obs_lower for word in ["spots", "brown spots", "black spots"]):
            return {
                "crop": crop,
                "issue": "Fungal infection (leaf spots)",
                "confidence": 65,
                "recommendation": "Remove affected leaves. Apply fungicide or neem oil spray. Improve air circulation.",
                "risk": "high",
                "method": "rule-based"
            }
        
        if any(word in obs_lower for word in ["wilting", "drooping", "droopy"]):
            return {
                "crop": crop,
                "issue": "Water stress or root damage",
                "confidence": 75,
                "recommendation": "Check soil moisture. Water deeply if dry. Check for root rot if soil is wet.",
                "risk": "medium",
                "method": "rule-based"
            }
        
        if any(word in obs_lower for word in ["holes", "eaten", "chewed"]):
            return {
                "crop": crop,
                "issue": "Pest damage (likely caterpillars or beetles)",
                "confidence": 70,
                "recommendation": "Hand-pick pests if visible. Apply neem oil or soap spray. Use companion planting.",
                "risk": "medium",
                "method": "rule-based"
            }
        
        if any(word in obs_lower for word in ["stunted", "small", "not growing"]):
            return {
                "crop": crop,
                "issue": "Nutrient deficiency or poor soil",
                "confidence": 60,
                "recommendation": "Add compost or balanced fertilizer. Check soil pH. Ensure adequate water.",
                "risk": "medium",
                "method": "rule-based"
            }
        
        # Default response
        return {
            "crop": crop,
            "issue": "Unable to diagnose - need more information",
            "confidence": 30,
            "recommendation": "Please send a photo of your crop via WhatsApp for better diagnosis. Describe: leaf color, spots, wilting, pests visible.",
            "risk": "unknown",
            "method": "rule-based"
        }

# ============================================================================
# WEATHER API (Free)
# ============================================================================

async def get_weather_free(location: str) -> Optional[Dict]:
    """
    Get weather data from Open-Meteo (free, no API key needed)
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Geocode location
            geo_response = await client.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
            )
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                if geo_data.get("results"):
                    lat = geo_data["results"][0]["latitude"]
                    lon = geo_data["results"][0]["longitude"]
                    
                    # Get weather
                    weather_response = await client.get(
                        f"https://api.open-meteo.com/v1/forecast?"
                        f"latitude={lat}&longitude={lon}"
                        f"&current_weather=true"
                        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
                        f"&timezone=auto"
                    )
                    
                    if weather_response.status_code == 200:
                        return weather_response.json()
        
        return None
    
    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return None

# ============================================================================
# WHATSAPP FUNCTIONS
# ============================================================================

async def send_whatsapp_message(to: str, message: str) -> bool:
    """Send WhatsApp message"""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print(f"Would send to {to}: {message}")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages",
                headers={
                    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": to,
                    "type": "text",
                    "text": {"body": message}
                }
            )
            return response.status_code == 200
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return False


async def send_whatsapp_image(to: str, image_url: str, caption: str) -> bool:
    """Send WhatsApp image with caption"""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages",
                headers={
                    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "messaging_product": "whatsapp",
                    "to": to,
                    "type": "image",
                    "image": {
                        "link": image_url,
                        "caption": caption
                    }
                }
            )
            return response.status_code == 200
    except Exception as e:
        print(f"Failed to send WhatsApp image: {e}")
        return False

# ============================================================================
# MESSAGE HANDLERS
# ============================================================================

async def handle_whatsapp_message(message: Dict):
    """Handle individual WhatsApp message"""
    try:
        from_number = message["from"]
        message_type = message["type"]
        
        # Get or create user
        user = await get_user_by_phone(from_number)
        
        if not user:
            # New user - send onboarding
            user = await create_user(from_number)
            await send_whatsapp_message(
                from_number,
                "👋 *Welcome to AgriAI!*\n\n"
                "I'm your free AI farming assistant.\n\n"
                "Send me:\n"
                "📸 Photo of your crop for diagnosis\n"
                "💬 Description of any issues\n"
                "❓ Any farming questions\n\n"
                "Let's start: What crop are you growing?"
            )
            return
        
        # Process based on message type
        if message_type == "text":
            text = message["text"]["body"]
            await handle_text_message(user, text)
        
        elif message_type == "image":
            image_id = message["image"]["id"]
            caption = message["image"].get("caption", "")
            await handle_image_message(user, image_id, caption)
        
        elif message_type == "audio":
            await send_whatsapp_message(
                from_number,
                "🎤 Voice messages coming soon! For now, please send text or photos."
            )
    
    except Exception as e:
        print(f"Error handling message: {e}")


async def handle_text_message(user: Dict, text: str):
    """Handle text message from farmer"""
    
    # Check for special commands
    if text.upper().startswith("JOIN "):
        await handle_referral(user, text)
        return
    
    if text.lower() in ["help", "menu", "start"]:
        await send_help_message(user["phone"])
        return
    
    # Regular diagnosis
    ai = FreeAIEngine()
    
    # Get weather if user has location
    weather = None
    if user.get("location"):
        weather = await get_weather_free(user["location"])
    
    # Run diagnosis
    diagnosis = await ai.diagnose_crop(
        crop=user.get("primary_crop", "unknown"),
        observations=text,
        location=user.get("location", "unknown"),
        weather=weather
    )
    
    # Save to database
    await save_diagnosis(user["id"], diagnosis)
    
    # Format response
    response = f"""🌾 *Diagnosis for {diagnosis['crop']}*

🔍 *Issue:* {diagnosis['issue']}
📊 *Confidence:* {diagnosis['confidence']}%

💡 *Recommended Action:*
{diagnosis['recommendation']}

⚠️ *Risk Level:* {diagnosis['risk']}

---
Was this helpful?
Reply: YES or NO for feedback

Need more help? Send a photo! 📸"""
    
    # Send response
    await send_whatsapp_message(user["phone"], response)


async def handle_image_message(user: Dict, image_id: str, caption: str):
    """Handle image message (crop photo)"""
    
    # For now, treat as text diagnosis with caption
    # TODO: Add computer vision in future
    
    await send_whatsapp_message(
        user["phone"],
        "📸 Photo received! Analyzing...\n\n"
        "(Note: Visual analysis coming soon. For now, please describe what you see in the photo.)"
    )
    
    if caption:
        await handle_text_message(user, caption)


async def handle_referral(user: Dict, text: str):
    """Handle referral code"""
    try:
        referral_code = text.split()[1].upper()
        
        # Find referrer
        if supabase:
            result = supabase.table("users").select("*").eq("referral_code", referral_code).execute()
            
            if result.data:
                referrer = result.data[0]
                
                # Update referrer's count
                new_count = referrer.get("referrals", 0) + 1
                supabase.table("users").update({
                    "referrals": new_count
                }).eq("id", referrer["id"]).execute()
                
                # Notify referrer
                if new_count >= 3:
                    await send_whatsapp_message(
                        referrer["phone"],
                        "🎉 *Congratulations!*\n\n"
                        f"You've referred {new_count} farmers!\n"
                        "Premium features unlocked! 🚀"
                    )
                else:
                    await send_whatsapp_message(
                        referrer["phone"],
                        f"✅ New referral! ({new_count}/3 for premium)"
                    )
                
                # Welcome new user
                await send_whatsapp_message(
                    user["phone"],
                    f"👋 Welcome! Referred by {referrer.get('name', 'a farmer')}.\n\n"
                    "You both get bonus credits! 🎁"
                )
            else:
                await send_whatsapp_message(
                    user["phone"],
                    "❌ Invalid referral code. Try again or skip."
                )
    
    except Exception as e:
        print(f"Referral error: {e}")


async def send_help_message(phone: str):
    """Send help/menu message"""
    await send_whatsapp_message(
        phone,
        "📋 *AgriAI Help Menu*\n\n"
        "🌾 *Get Diagnosis:*\n"
        "Just describe your crop issue or send a photo\n\n"
        "🔗 *Refer Friends:*\n"
        "Share your code, earn rewards!\n\n"
        "💬 *Commands:*\n"
        "• HELP - Show this menu\n"
        "• JOIN [code] - Use referral code\n\n"
        "Questions? Just ask!"
    )

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with simple dashboard"""
    
    # Get stats
    user_count = 0
    diagnosis_count = 0
    recent_diagnoses = []
    
    if supabase:
        try:
            users = supabase.table("users").select("*", count="exact").execute()
            user_count = users.count or 0
            
            diagnoses = supabase.table("diagnoses").select("*").order("created_at", desc=True).limit(10).execute()
            diagnosis_count = len(diagnoses.data)
            recent_diagnoses = diagnoses.data
        except:
            pass
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AgriAI Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }}
            .header h1 {{
                font-size: 3em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .stat-card h2 {{
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .stat-card p {{
                color: #666;
                font-size: 1.1em;
            }}
            .recent {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .recent h3 {{
                color: #667eea;
                margin-bottom: 20px;
                font-size: 1.5em;
            }}
            .diagnosis-item {{
                padding: 15px;
                border-left: 4px solid #667eea;
                background: #f8f9fa;
                margin-bottom: 10px;
                border-radius: 5px;
            }}
            .diagnosis-item strong {{
                color: #333;
            }}
            .diagnosis-item span {{
                color: #666;
                font-size: 0.9em;
            }}
            .footer {{
                text-align: center;
                color: white;
                margin-top: 40px;
                opacity: 0.8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 AgriAI</h1>
                <p>Zero Capital Edition - Free AI Farming Assistant</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h2>{user_count}</h2>
                    <p>Total Farmers</p>
                </div>
                <div class="stat-card">
                    <h2>{diagnosis_count}</h2>
                    <p>Diagnoses Today</p>
                </div>
                <div class="stat-card">
                    <h2>$0</h2>
                    <p>Monthly Cost</p>
                </div>
            </div>
            
            <div class="recent">
                <h3>🔬 Recent Diagnoses</h3>
                {''.join([f'''
                <div class="diagnosis-item">
                    <strong>{d.get("crop", "Unknown")}</strong>: {d.get("issue", "N/A")} 
                    <span>({d.get("confidence", 0)}% confidence)</span>
                </div>
                ''' for d in recent_diagnoses]) if recent_diagnoses else '<p>No diagnoses yet</p>'}
            </div>
            
            <div class="footer">
                <p>Built with ❤️ by a 19-year-old student</p>
                <p>Running on free tier: Railway + Supabase + WhatsApp + Groq</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if supabase else "not configured",
        "whatsapp": "configured" if WHATSAPP_TOKEN else "not configured"
    }


@app.get("/webhook/whatsapp")
async def whatsapp_webhook_verify(request: Request):
    """Verify WhatsApp webhook (GET request from Meta)"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        print("✅ WhatsApp webhook verified!")
        return int(challenge)
    
    return JSONResponse({"error": "Verification failed"}, status_code=403)


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive WhatsApp messages"""
    try:
        data = await request.json()
        
        # Process in background to respond quickly
        background_tasks.add_task(process_whatsapp_webhook, data)
        
        return {"status": "ok"}
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}


async def process_whatsapp_webhook(data: Dict):
    """Process WhatsApp webhook data in background"""
    try:
        if data.get("object") != "whatsapp_business_account":
            return
        
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                if "messages" in value:
                    for message in value["messages"]:
                        await handle_whatsapp_message(message)
    
    except Exception as e:
        print(f"Error processing webhook: {e}")


@app.get("/stats")
async def get_stats():
    """Get platform statistics"""
    if not supabase:
        return {"error": "Database not configured"}
    
    try:
        users = supabase.table("users").select("*", count="exact").execute()
        diagnoses = supabase.table("diagnoses").select("*", count="exact").execute()
        
        return {
            "total_users": users.count or 0,
            "total_diagnoses": diagnoses.count or 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n" + "="*60)
    print("🚀 AgriAI - Zero Capital Edition Starting...")
    print("="*60)
    print(f"📱 WhatsApp Phone ID: {WHATSAPP_PHONE_ID or 'Not configured'}")
    print(f"💾 Database: {SUPABASE_URL or 'Not configured'}")
    print(f"🤖 AI Engine: {'Groq (Free)' if GROQ_API_KEY else 'Rule-based only'}")
    print("="*60 + "\n")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️  WARNING: Supabase not configured. Using in-memory storage.")
    
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print("⚠️  WARNING: WhatsApp not configured. Messages will be logged only.")
    
    print("✅ Server ready!\n")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
