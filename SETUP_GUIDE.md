# 🚀 Message Forwarder Bot Setup Guide

## 📋 **প্রথমে যা করতে হবে (What to do first):**

### 1. **`.env` ফাইল তৈরি করুন (Create .env file):**
- আপনার workspace-এ `.env` নামে একটি নতুন ফাইল তৈরি করুন
- `env_example.txt` থেকে content copy করে `.env` ফাইলে paste করুন

### 2. **API Credentials যোগ করুন (Add API Credentials):**
```env
# আপনার actual values দিন (Fill in your actual values):
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
PHONE=+8801234567890
```

### 3. **Group IDs যোগ করুন (Add Group IDs):**
```env
# Source groups (যেখান থেকে message forward হবে):
SOURCE_GROUP_IDS=123456789,987654321,111222333

# Target group (যেখানে message forward হবে):
TARGET_GROUP_ID=555666777
```

## 🔧 **Configuration Steps:**

### Step 1: Telegram API Setup
1. [my.telegram.org](https://my.telegram.org) এ যান
2. Login করুন
3. "API development tools" এ click করুন
4. New application তৈরি করুন
5. `API_ID` এবং `API_HASH` copy করুন

### Step 2: Group IDs Find করুন
1. Source group এ যান
2. Group info → Group type দেখুন
3. Public group হলে: `@groupname` থেকে ID বের করুন
4. Private group হলে: Bot add করে ID বের করুন

### Step 3: .env File Update করুন
```env
# Example configuration:
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890
PHONE=+8801234567890

SOURCE_GROUP_IDS=123456789,987654321,111222333
SOURCE_GROUP_NAMES=Sam's Group,Raaf's Group,Mr Sunny's Group

TARGET_GROUP_ID=555666777
MESSAGE_DELAY=2
```

## 🧪 **Test Configuration:**

Configuration test করার জন্য:
```bash
python test_config.py
```

## 🚀 **Bot চালু করুন:**

```bash
python bot.py
```

## ❌ **Common Problems & Solutions:**

### Problem 1: "API_ID not found"
**Solution:** `.env` ফাইল তৈরি করুন এবং API credentials যোগ করুন

### Problem 2: "Group ID not found"
**Solution:** Actual group IDs ব্যবহার করুন, example IDs নয়

### Problem 3: "Session file error"
**Solution:** `session_name.session` ফাইল delete করে আবার চালু করুন

### Problem 4: "Phone number error"
**Solution:** Phone number format: `+8801234567890` (country code সহ)

## 📱 **Bot Features:**

✅ **Multiple source groups** support  
✅ **Automatic price calculation** (watches vs non-watches)  
✅ **Source group identification** (S, R, M, A, J letters)  
✅ **Custom delivery messages** per group  
✅ **Media forwarding** (photos, videos, documents)  
✅ **Contact info** auto-append  

## 🔍 **Debug Tips:**

1. **Logs check করুন:** Bot চালু করার সময় console logs দেখুন
2. **Group permissions:** Bot group এ admin permissions আছে কিনা check করুন
3. **Session file:** `session_name.session` ফাইল corrupt হলে delete করুন
4. **Environment variables:** `.env` ফাইল properly load হচ্ছে কিনা check করুন

## 📞 **Help:**

যদি এখনও সমস্যা থাকে:
1. `test_config.py` run করে output দেখান
2. Bot run করার সময় error message copy করে দিন
3. `.env` ফাইলের content (sensitive info hide করে) share করুন
