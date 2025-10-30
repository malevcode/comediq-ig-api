from ig_messaging import InstagramMessagingSystem

# Initialize the messaging system
messaging_system = InstagramMessagingSystem()

# Load CSV and send messages
csv_file = "active_to_confirm_NY.csv"
username_column = "changes_updates"

# Your message
MSG = "Yo I'm doing a monthly verification of every open mic on my platform! Can you confirm that your mic is active and lmk about any changes?"

# Send messages from CSV
results = messaging_system.send_messages_from_csv(csv_file, username_column, MSG)

# Print results summary
print("\n" + "="*60)
print("📤 SENDING COMPLETE")
print("="*60)

successful = sum(1 for r in results.values() if not isinstance(r, str) or not r.startswith("User") and not r.startswith("Error"))
print(f"✅ Successfully sent: {successful}/{len(results)}")

# Show errors
for username, result in results.items():
    if isinstance(result, str) and (result.startswith("User") or result.startswith("Error")):
        print(f"❌ {username}: {result}")

# Print status report
messaging_system.print_status_report()

print("\n💡 To collect responses later, run: python collect_messages.py")
print("="*60)