import json
import sqlite3

def run_reconciliation():
    #Load DATA
    with open ('hr_source.json', 'r') as hr_file:
        hr_data = json.load(hr_file)

    with open('target_system.json','r') as target_file:
        target_data = json.load(target_file)

    #Transform for Speed
    active_hr_ids = {user['id'] for user in hr_data if user ['status'] == 'Active'} 


    #Governance Logic
    stale_accounts = []
    for account in target_data:
        if account ['id'] not in active_hr_ids:
            stale_accounts.append(account)

    #Output RISK
    if stale_accounts:
        print(f"vv ALERT: {len(stale_accounts)} STALE ACCOUNT(S) FOUND vv")
        for acc in stale_accounts:
            print(f"ACTION REQUIRED: Remove access for {acc['account_name']} (ID: {acc['id']})")
    else:
        print("System clean no stale accounts")


def mover(old_records, new_records):
    old_map = {user['id']: user for user in old_records}
    movers_detected = []

    for new_user in new_records:
        user_id = new_user['id']
        
        #check if user existed in the old data
        if user_id in old_map:
            old_user = old_map[user_id]

            #Mover LOGIC
            if old_user['department'] != new_user['department']:
                movers_detected.append({
                    'id': user_id,
                    'name': new_user['name'],
                    'old_dept': old_user['department'],
                    'new_dept': new_user['department']
                })
    return movers_detected



if __name__ == '__main__':
    old_hr = [{"id": "101", "name": "Alice", "department": "Sales"}]
    new_hr = [{"id": "101", "name": "Alice", "department": "Engineering"}]
    changes = mover(old_hr, new_hr)
    for change in changes:
        print(f"MOVER ALERT: {change['name']} moved from {change['old_dept']} -> {change['new_dept']}")
    run_reconciliation()
