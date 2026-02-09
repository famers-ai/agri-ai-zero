# 🎯 30-Minute Deployment Checklist

**Follow this checklist to deploy AgriAI in 30 minutes**

Print this page and check off each step as you complete it.

---

## ⏱️ Time Budget

- [ ] **10 min** - Supabase setup
- [ ] **5 min** - Groq AI setup  
- [ ] **10 min** - WhatsApp Business setup
- [ ] **5 min** - Railway deployment
- [ ] **5 min** - Testing

**Total: 35 minutes** (with 5 min buffer)

---

## 📋 Pre-Deployment

- [ ] GitHub account ready
- [ ] Gmail account ready
- [ ] Phone number for WhatsApp (can be personal)
- [ ] This checklist printed or open

---

## 1️⃣ Supabase (10 min)

- [ ] Go to supabase.com
- [ ] Sign up with GitHub
- [ ] Create new project named "agri-ai"
- [ ] Wait for project to initialize (2-3 min)
- [ ] Open SQL Editor
- [ ] Copy `database/schema.sql` contents
- [ ] Paste and run SQL
- [ ] Verify "Success" message
- [ ] Go to Settings → API
- [ ] Copy **Project URL**: `________________`
- [ ] Copy **anon key**: `________________`

---

## 2️⃣ Groq AI (5 min)

- [ ] Go to console.groq.com
- [ ] Sign up with Gmail
- [ ] Verify email
- [ ] Click "API Keys"
- [ ] Create new API key named "agri-ai"
- [ ] Copy API key: `________________`
- [ ] Save it (can't see again!)

---

## 3️⃣ WhatsApp Business (10 min)

- [ ] Go to business.facebook.com
- [ ] Create Business account
- [ ] Verify email
- [ ] Click "WhatsApp" in menu
- [ ] Click "Get Started"
- [ ] Add phone number
- [ ] Verify with SMS code
- [ ] Complete business profile
- [ ] Go to Configuration
- [ ] Copy **Phone Number ID**: `________________`
- [ ] Copy **Access Token**: `________________`

---

## 4️⃣ Railway (5 min)

- [ ] Go to railway.app
- [ ] Sign in with GitHub
- [ ] Fork AgriAI repo to your GitHub
- [ ] In Railway, click "New Project"
- [ ] Click "Deploy from GitHub repo"
- [ ] Select your forked repo
- [ ] Wait for initial deploy
- [ ] Click on service → "Variables"
- [ ] Add environment variables:

```
SUPABASE_URL=________________
SUPABASE_KEY=________________
WHATSAPP_ACCESS_TOKEN=________________
WHATSAPP_PHONE_ID=________________
WEBHOOK_VERIFY_TOKEN=my_secret_123
GROQ_API_KEY=________________
PORT=8000
```

- [ ] Click "Deploy" to restart
- [ ] Go to Settings → Domains
- [ ] Click "Generate Domain"
- [ ] Copy URL: `________________`

---

## 5️⃣ Connect WhatsApp (5 min)

- [ ] Go back to Meta Business Manager
- [ ] WhatsApp → Configuration
- [ ] Click "Edit" next to Webhook
- [ ] Callback URL: `https://your-app.railway.app/webhook/whatsapp`
- [ ] Verify Token: `my_secret_123`
- [ ] Click "Verify and Save"
- [ ] Should see green checkmark ✅
- [ ] Click "Subscribe" next to "messages"

---

## 6️⃣ Testing (5 min)

- [ ] Open Railway URL in browser
- [ ] See dashboard with 0 users
- [ ] Save WhatsApp Business number to phone
- [ ] Send message: "Hello"
- [ ] Receive onboarding message
- [ ] Send: "My tomato leaves are yellow"
- [ ] Receive AI diagnosis
- [ ] Check Railway logs (no errors)
- [ ] Check Supabase (user created)

---

## ✅ Deployment Complete!

**Congratulations!** Your AgriAI platform is live.

### What You Built:

✅ Production-ready AI farming assistant  
✅ WhatsApp integration  
✅ Free AI inference  
✅ Database with user management  
✅ Beautiful admin dashboard  
✅ Referral system  
✅ Feedback collection  

### Cost: $0/month

---

## 🎯 Next Steps

- [ ] Test all features thoroughly
- [ ] Onboard first real farmer
- [ ] Get feedback
- [ ] Iterate and improve
- [ ] Scale to 10 farmers this week

---

## 📞 Troubleshooting

**If something doesn't work:**

1. Check Railway logs
2. Verify all environment variables
3. Check WhatsApp webhook is subscribed
4. Refer to `docs/DEPLOYMENT_GUIDE.md`

---

## 🎉 You Did It!

**Time taken**: _____ minutes

**You just deployed a production platform with $0.**

Now go change the world! 🌾

---

**Deployment Date**: ________________  
**Railway URL**: ________________  
**WhatsApp Number**: ________________  

**First Farmer Onboarded**: ________________  
**Date**: ________________
