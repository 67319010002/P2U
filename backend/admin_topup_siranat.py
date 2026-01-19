from mongoengine import connect
from models import User, WalletHistory
import datetime

from config import Config

# Connect to MongoDB using settings from Config
connect(
    db=Config.MONGODB_SETTINGS['db'],
    host=Config.MONGODB_SETTINGS['host']
)

from mongoengine.connection import get_db

def topup_siranat():
    # Debug Connection
    try:
        db = get_db()
        print(f"🔌 Connected to Database: {db.name}")
        params = Config.MONGODB_SETTINGS
        print(f"📝 Config DB: {params.get('db')}")
        # Mask password for printing
        host = params.get('host', '')
        masked = host.split('@')[-1] if '@' in host else 'localhost'
        print(f"🌐 Host: ...@{masked}")
        
        count = User.objects.count()
        print(f"👥 Total Users in DB: {count}")
    except Exception as e:
        print(f"💥 Connection/Query Error: {e}")
        return

    # Find user "Siranat"
    # Using case-insensitive regex search just in case
    user = User.objects(username__iexact="Siranat").first()
    
    if not user:
        print("❌ User 'Siranat' not found!")
        print("Available users:")
        for u in User.objects()[:10]: # Limit to 10
            print(f"- {u.username} (ID: {u.id})")
        return

    amount = 30000
    balance_before = user.token_balance or 0
    
    # Update Balance
    user.token_balance = balance_before + amount
    user.save()
    
    # Create History Record
    WalletHistory(
        user=user,
        type='topup',
        amount=amount,
        balance_before=balance_before,
        balance_after=user.token_balance,
        description="Admin Manual Top-up (Special Grant)",
        reference_id="ADMIN_GRANT_001",
        created_at=datetime.datetime.utcnow()
    ).save()
    
    print(f"✅ Successfully added {amount} tokens to 'Siranat'")
    print(f"💰 Old Balance: {balance_before}")
    print(f"💰 New Balance: {user.token_balance}")

if __name__ == "__main__":
    topup_siranat()
