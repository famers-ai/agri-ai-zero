# 🚀 Complete Deployment Guide

**Get AgriAI running in 30 minutes with $0 budget**

## Prerequisites

- GitHub account (free)
- Gmail account (for other services)
- 30 minutes of time
- That's it!

---

## Step-by-Step Deployment

### 1️⃣ Supabase Setup (10 minutes)

#### Create Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub
4. No credit card needed!

#### Create Project
1. Click "New Project"
2. Choose organization (create if needed)
3. Project settings:
   - **Name**: `agri-ai`
   - **Database Password**: (generate strong password)
   - **Region**: Choose closest to your users
4. Click "Create new project"
5. Wait 2-3 minutes for setup

#### Set Up Database
1. Click "SQL Editor" in sidebar
2. Click "New query"
3. Copy entire contents of `database/schema.sql`
4. Paste and click "Run"
5. Should see "Success. No rows returned"

#### Get API Credentials
1. Click "Settings" → "API"
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJhbGc...` (long string)
3. Save these for later!

---

### 2️⃣ Groq AI Setup (5 minutes)

#### Create Account
1. Go to [console.groq.com](https://console.groq.com)
2. Click "Sign up"
3. Use Gmail to sign up
4. Verify email

#### Get API Key
1. Click "API Keys" in sidebar
2. Click "Create API Key"
3. Name: `agri-ai`
4. Copy the key (starts with `gsk_...`)
5. Save it! (You can't see it again)

---

### 3️⃣ WhatsApp Business Setup (10 minutes)

#### Create Meta Business Account
1. Go to [business.facebook.com](https://business.facebook.com)
2. Click "Create Account"
3. Follow the prompts
4. Verify your email

#### Set Up WhatsApp
1. In Business Manager, click "WhatsApp"
2. Click "Get Started"
3. Choose "Use WhatsApp Business API"
4. Follow setup wizard:
   - Add phone number (can be your personal number)
   - Verify with SMS code
   - Set up business profile

#### Get API Credentials
1. Go to WhatsApp → Configuration
2. Copy these values:
   - **Phone Number ID**: (numeric ID)
   - **Access Token**: (click "Copy" button)
3. Save these!

#### Important Notes
- Free tier: 1,000 conversations/month
- A "conversation" = 24-hour window with a user
- Plenty for starting out!

---

### 4️⃣ Railway Deployment (5 minutes)

#### Create Account
1. Go to [railway.app](https://railway.app)
2. Click "Login"
3. Sign in with GitHub
4. Authorize Railway

#### Deploy Project

**Option A: From GitHub (Recommended)**

1. Fork this repo to your GitHub
2. In Railway, click "New Project"
3. Click "Deploy from GitHub repo"
4. Select your forked repo
5. Railway auto-detects Python and deploys!

**Option B: From Template**

1. Click "New Project"
2. Click "Deploy from template"
3. Search for "FastAPI"
4. Use the template

#### Add Environment Variables

1. Click on your deployed service
2. Click "Variables" tab
3. Add these variables:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
WHATSAPP_ACCESS_TOKEN=EAAxxxxx...
WHATSAPP_PHONE_ID=123456789
WEBHOOK_VERIFY_TOKEN=my_secret_verify_token_123
GROQ_API_KEY=gsk_xxxxx...
PORT=8000
```

4. Click "Deploy" to restart with new variables

#### Get Your URL

1. Click "Settings" tab
2. Under "Domains", click "Generate Domain"
3. Copy your URL: `https://your-app.railway.app`
4. Save it!

---

### 5️⃣ Connect WhatsApp Webhook (5 minutes)

#### Configure Webhook

1. Go back to Meta Business Manager
2. WhatsApp → Configuration
3. Click "Edit" next to Webhook
4. Enter:
   - **Callback URL**: `https://your-app.railway.app/webhook/whatsapp`
   - **Verify Token**: `my_secret_verify_token_123` (same as env var)
5. Click "Verify and Save"

#### Subscribe to Events

1. Under "Webhook fields"
2. Click "Subscribe" next to:
   - ✅ messages
3. That's it!

---

### 6️⃣ Test Your Deployment (5 minutes)

#### Check Dashboard

1. Open your Railway URL in browser
2. Should see beautiful dashboard
3. Stats should show 0 users, 0 diagnoses

#### Test WhatsApp

1. Save your WhatsApp Business number
2. Send a message: "Hello"
3. Should get onboarding message!
4. Try: "My tomato leaves are yellow"
5. Should get AI diagnosis! 🎉

#### Verify Everything Works

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Should return:
{
  "status": "healthy",
  "database": "connected",
  "whatsapp": "configured"
}
```

---

## 🎉 You're Live!

Congratulations! Your AgriAI platform is now running on:
- ✅ Railway (free hosting)
- ✅ Supabase (free database)
- ✅ WhatsApp Business (free messaging)
- ✅ Groq AI (free inference)

**Total cost: $0/month**

---

## 🐛 Troubleshooting

### WhatsApp webhook not working

**Problem**: Messages not reaching your server

**Solutions**:
1. Check Railway logs: Click "Deployments" → Latest deployment → "View Logs"
2. Verify webhook URL is correct (no typos)
3. Verify token matches exactly
4. Check WhatsApp is subscribed to "messages" event

### Database errors

**Problem**: "Database not configured" error

**Solutions**:
1. Verify `SUPABASE_URL` and `SUPABASE_KEY` are set in Railway
2. Check Supabase project is active (not paused)
3. Verify schema was created (check Supabase Table Editor)

### AI not responding

**Problem**: Getting rule-based responses only

**Solutions**:
1. Check `GROQ_API_KEY` is set correctly
2. Verify Groq API key is active (test at console.groq.com)
3. Check Railway logs for API errors

### Railway deployment failed

**Problem**: Deployment shows error

**Solutions**:
1. Check `requirements.txt` is present
2. Verify Python version (should use 3.11+)
3. Check Railway logs for specific error
4. Ensure `PORT` environment variable is set

---

## 📊 Monitoring

### Check Logs

**Railway**:
1. Go to your project
2. Click "Deployments"
3. Click latest deployment
4. Click "View Logs"

**Supabase**:
1. Go to your project
2. Click "Logs"
3. Filter by table or time

### Monitor Usage

**Railway**:
- Free tier: $5 credit/month
- Check usage: Settings → Usage

**Supabase**:
- Free tier: 500MB database
- Check usage: Settings → Usage

**WhatsApp**:
- Free tier: 1,000 conversations/month
- Check usage: Meta Business Manager → WhatsApp → Insights

---

## 🔄 Updates & Maintenance

### Update Code

1. Make changes to your code
2. Commit to GitHub:
```bash
git add .
git commit -m "Update: description"
git push origin main
```
3. Railway auto-deploys!

### Update Database Schema

1. Go to Supabase SQL Editor
2. Run new SQL commands
3. Changes are immediate

### Update Environment Variables

1. Go to Railway → Variables
2. Edit or add variables
3. Click "Deploy" to restart

---

## 🎯 Next Steps

Now that you're deployed:

1. **Test thoroughly**
   - Send various messages
   - Try different crop issues
   - Test referral system

2. **Onboard first farmer**
   - Find a real farmer
   - Walk them through it
   - Get feedback

3. **Monitor and iterate**
   - Check logs daily
   - Fix any issues
   - Improve based on feedback

4. **Scale gradually**
   - Week 1: 10 farmers
   - Week 4: 30 farmers
   - Week 8: 100 farmers

---

## 💡 Pro Tips

### Save Money
- Railway gives $5/month free
- That's enough for ~500 active users
- Monitor usage to avoid overages

### Improve Performance
- Use caching for weather data
- Batch database queries
- Optimize AI prompts

### Scale Efficiently
- Start with rule-based fallback
- Add AI as you grow
- Use AI only for complex cases

---

## 🆘 Need Help?

### Common Issues

**"Webhook verification failed"**
→ Check verify token matches exactly

**"Database connection error"**
→ Verify Supabase credentials

**"WhatsApp not sending"**
→ Check access token is valid

**"AI not working"**
→ Verify Groq API key

### Get Support

1. Check Railway logs first
2. Check Supabase logs
3. Open GitHub issue
4. Email: your-email@example.com

---

## ✅ Deployment Checklist

Before going live:

- [ ] Supabase project created
- [ ] Database schema deployed
- [ ] Groq API key obtained
- [ ] WhatsApp Business set up
- [ ] Railway project deployed
- [ ] Environment variables set
- [ ] Webhook configured
- [ ] Health check passes
- [ ] Dashboard accessible
- [ ] WhatsApp test successful
- [ ] AI diagnosis working

---

**You're ready to change the world! 🚀**

**Total setup time**: ~30 minutes  
**Total cost**: $0  
**Potential impact**: Unlimited

Go onboard your first farmer! 🌾
