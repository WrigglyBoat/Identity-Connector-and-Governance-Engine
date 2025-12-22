import json

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

if __name__ == '__main__':
    run_reconciliation()
