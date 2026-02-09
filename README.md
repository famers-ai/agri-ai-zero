# 🌾 AgriAI - Zero Capital Edition

**A complete AI farming assistant that runs on $0/month**

Built by a 19-year-old student to help smallholder farmers worldwide access AI-powered agricultural advice via WhatsApp.

## 🎯 What This Is

- **Free AI farming assistant** via WhatsApp
- **Zero infrastructure costs** (free tiers only)
- **Production-ready** monolith architecture
- **1-person manageable** codebase
- **Sustainable revenue model** (data marketplace)

## 💰 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Railway (hosting) | $5 credit/month | $0 |
| Supabase (database) | 500MB | $0 |
| WhatsApp Business | 1,000 conversations/month | $0 |
| Groq AI | Free tier | $0 |
| Open-Meteo (weather) | Unlimited | $0 |
| **TOTAL** | | **$0/month** |

## 🚀 Quick Start (30 minutes)

### Step 1: Create Free Accounts

1. **Supabase** (database)
   - Go to [supabase.com](https://supabase.com)
   - Create account (no credit card needed)
   - Create new project
   - Copy URL and anon key

2. **Railway** (hosting)
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Get $5 free credit

3. **Meta Business** (WhatsApp)
   - Go to [business.facebook.com](https://business.facebook.com)
   - Create Business account
   - Set up WhatsApp Business API
   - Get access token and phone ID

4. **Groq** (AI)
   - Go to [console.groq.com](https://console.groq.com)
   - Create account
   - Get API key (free tier)

### Step 2: Set Up Database

1. Open Supabase SQL Editor
2. Copy contents of `database/schema.sql`
3. Run the SQL script
4. Verify tables are created

### Step 3: Deploy to Railway

1. Fork this repo to your GitHub
2. In Railway, click "New Project"
3. Select "Deploy from GitHub"
4. Choose your forked repo
5. Add environment variables:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_phone_id
WEBHOOK_VERIFY_TOKEN=any_random_string_123
GROQ_API_KEY=your_groq_key
```

6. Railway will auto-deploy!
7. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### Step 4: Configure WhatsApp Webhook

1. In Meta Business Manager
2. Go to WhatsApp → Configuration
3. Set webhook URL: `https://your-app.railway.app/webhook/whatsapp`
4. Set verify token: (same as `WEBHOOK_VERIFY_TOKEN` above)
5. Subscribe to `messages` events
6. Done!

### Step 5: Test It!

1. Save your WhatsApp Business number
2. Send a message: "Hello"
3. Bot should respond with onboarding
4. Try: "My tomato leaves are yellow"
5. Get AI diagnosis! 🎉

## 📱 How It Works

### For Farmers

1. **Send WhatsApp message** to your business number
2. **Describe crop issue** or send photo
3. **Get instant AI diagnosis** with recommendations
4. **Earn money** from anonymized data contributions

### For You

1. **Monitor dashboard** at your Railway URL
2. **Track users and diagnoses**
3. **Improve AI** with farmer feedback
4. **Scale sustainably** with data marketplace

## 🏗️ Architecture

```
┌─────────────┐
│   Farmer    │
│  (WhatsApp) │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  WhatsApp Business  │
│    (Free Tier)      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   FastAPI Backend   │
│   (Railway $0)      │
│                     │
│  ┌──────────────┐   │
│  │  AI Engine   │   │
│  │  (Groq Free) │   │
│  └──────────────┘   │
│                     │
│  ┌──────────────┐   │
│  │ Rule-Based   │   │
│  │  Fallback    │   │
│  └──────────────┘   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Supabase Database  │
│    (Free 500MB)     │
└─────────────────────┘
```

## 📊 Features

### ✅ Current (v1.0)

- [x] WhatsApp integration
- [x] AI-powered diagnosis (Groq)
- [x] Rule-based fallback
- [x] Weather integration
- [x] User management
- [x] Referral system
- [x] Admin dashboard
- [x] Feedback collection

### 🚧 Coming Soon

- [ ] Image-based diagnosis (computer vision)
- [ ] Voice message support
- [ ] Multi-language support
- [ ] Data marketplace API
- [ ] Farmer earnings dashboard
- [ ] Premium features

## 💡 Usage Examples

### Text Diagnosis

```
Farmer: My tomato leaves are turning yellow

AgriAI: 🌾 Diagnosis for tomato

🔍 Issue: Nitrogen deficiency (yellowing leaves)
📊 Confidence: 70%

💡 Recommended Action:
Apply urea fertilizer (50kg per hectare) or compost. 
Water regularly.

⚠️ Risk Level: medium
```

### Referral System

```
Farmer: JOIN ABC123

AgriAI: 👋 Welcome! Referred by John.
You both get bonus credits! 🎁
```

## 📈 Growth Strategy

### Week 1: First 10 Farmers
- Personal onboarding
- Daily feedback
- Fix bugs immediately

### Week 4: 30 Farmers
- Referral system active
- WhatsApp group created
- Success stories shared

### Week 8: 100 Farmers
- NGO partnership
- University collaboration
- First revenue

### Week 12: 500+ Farmers
- Data marketplace live
- Sustainable revenue
- Viral growth

## 💰 Revenue Model

### Phase 1: Free for Farmers
- All features free
- Build user base
- Collect data

### Phase 2: Data Marketplace
- Sell aggregated insights to:
  - Fertilizer companies
  - Seed companies
  - Insurance companies
  - Researchers
- Farmers get 80% of revenue
- Platform keeps 20%

### Phase 3: Premium Features
- Free tier (forever)
- Premium ($2/month)
  - Advanced AI
  - Priority support
  - Historical tracking

## 🛠️ Development

### Local Development

```bash
# Clone repo
git clone <your-repo>
cd agri-ai-zero/backend

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp ../.env.example .env
# Edit .env with your values

# Run locally
python main.py
```

Visit `http://localhost:8000` to see dashboard

### Project Structure

```
agri-ai-zero/
├── backend/
│   ├── main.py              # Complete backend (monolith)
│   └── requirements.txt     # Python dependencies
├── database/
│   └── schema.sql          # Supabase schema
├── docs/
│   └── setup-guide.md      # Detailed setup
├── .env.example            # Environment template
└── README.md               # This file
```

## 🤝 Contributing

This is a solo project for now, but feedback welcome!

## 📄 License

MIT License - Free to use, modify, and distribute

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Supabase](https://supabase.com/) - Database
- [Railway](https://railway.app/) - Hosting
- [Groq](https://groq.com/) - AI inference
- [WhatsApp Business](https://business.whatsapp.com/) - Communication

## 📞 Support

- **Issues**: Open a GitHub issue
- **Questions**: Create a discussion
- **Email**: your-email@example.com

## 🌍 Impact

**Goal**: Help 10,000 smallholder farmers in first year

**Metrics**:
- Farmers served: 0 → 10,000
- Diagnoses provided: 0 → 100,000
- Farmer earnings: $0 → $50,000
- Infrastructure cost: $0 (always)

---

**Built with ❤️ by a 19-year-old student**

*Proving that you don't need capital to change the world.*

**Start date**: 2026-02-08  
**Status**: 🚀 Ready to launch

---

## 🎯 Next Steps

1. ✅ Set up free accounts (30 min)
2. ✅ Deploy to Railway (10 min)
3. ✅ Configure WhatsApp (5 min)
4. ✅ Test with yourself (5 min)
5. 🎯 Onboard first farmer (today!)
6. 🎯 Get to 10 farmers (this week)
7. 🎯 Reach 100 farmers (this month)
8. 🎯 Hit 1,000 farmers (90 days)

**The world is waiting. Let's go! 🚀**
