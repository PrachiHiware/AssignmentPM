import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error

def find_file(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.getcwd(), filename),
        os.path.join(script_dir, filename),
        os.path.join(script_dir, "..", filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return None

def find_data_dir():
    if "TALENTFLOW_DATA_DIR" in os.environ:
        return os.environ["TALENTFLOW_DATA_DIR"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(os.getcwd(), "data"),
        os.path.join(script_dir, "data"),
        os.path.join(script_dir, "..", "data")
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.abspath(os.path.join(script_dir, "..", "data"))

def load_env(env_path=None):
    if env_path is None:
        env_file = find_file(".env")
        if env_file:
            env_path = env_file
        else:
            return
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def fetch_table(base_id, table_name, token, output_dir=None):
    if output_dir is None:
        output_dir = find_data_dir()
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "TalentFlow-Data-Fetcher/1.0"
    }
    
    encoded_table = urllib.parse.quote(table_name)
    base_url = f"https://api.airtable.com/v0/{base_id}/{encoded_table}"
    
    records = []
    offset = None
    page = 1
    
    print(f"Fetching table: '{table_name}'...")
    
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}"
        
        req = urllib.request.Request(url, headers=headers)
        
        # Rate limit safety delay: 0.25s guarantees <= 4 requests/sec (Airtable limit is 5 req/sec)
        time.sleep(0.25)
        
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                page_records = data.get("records", [])
                records.extend(page_records)
                print(f"  Page {page}: fetched {len(page_records)} records (total so far: {len(records)})")
                
                offset = data.get("offset")
                if not offset:
                    break
                page += 1
                
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  Rate limited (429)! Waiting 30 seconds before retrying...")
                time.sleep(30)
                continue
            else:
                err_body = e.read().decode("utf-8", errors="replace")
                print(f"  Error fetching '{table_name}': HTTP {e.code} - {err_body}")
                raise
                
    safe_name = table_name.replace(" ", "_")
    output_path = os.path.join(output_dir, f"{safe_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    print(f"-> Saved {len(records)} records for '{table_name}' to {output_path}\n")
    return len(records)

def main():
    load_env()
    token = os.environ.get("AIRTABLE_TOKEN")
    base_id = os.environ.get("AIRTABLE_BASE_ID", "appYePRAI75PMbQNQ")
    
    if not token:
        print("Note: AIRTABLE_TOKEN not set in environment or .env file.", file=sys.stderr)
        print("Pre-cached JSON files are already available in the 'data/' directory.", file=sys.stderr)
        print("To re-fetch live data, create a .env file with AIRTABLE_TOKEN=<your_token>.", file=sys.stderr)
        sys.exit(1)
        
    tables = [
        "Departments",
        "People",
        "Job Openings",
        "Candidates",
        "Applications",
        "Interviews",
        "Offers",
        "Findings"
    ]
    
    output_dir = find_data_dir()
    os.makedirs(output_dir, exist_ok=True)
    
    summary = {}
    print(f"Starting fetch from Airtable base {base_id} into '{output_dir}/'...")
    start_time = time.time()
    
    for table in tables:
        count = fetch_table(base_id, table, token, output_dir)
        summary[table] = count
        
    elapsed = time.time() - start_time
    print("=" * 40)
    print(f"Fetch completed in {elapsed:.2f} seconds.")
    print("Record summary:")
    for tbl, count in summary.items():
        print(f"  - {tbl}: {count} records")
        
    with open(os.path.join(output_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "elapsed_seconds": elapsed}, f, indent=2)

if __name__ == "__main__":
    main()
