#!/usr/bin/env python3
"""
Simple script to convert weight JSON file to FIT format.
Usage: python json_to_fit.py <input_json_file> [output_fit_file]
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from garmin.fit_generator import create_weight_fit_file
from garmin.client import GarminClient

def main():
    # Delete old garmin-fit directory
    import shutil
    garmin_fit_dir = Path(__file__).parent.parent / "garmin-fit"
    if garmin_fit_dir.exists():
        shutil.rmtree(garmin_fit_dir)
        print(f"🗑️  Deleted directory: {garmin_fit_dir}")
    
    parser = argparse.ArgumentParser(description="Convert weight JSON to FIT file")
    parser.add_argument("input_file", help="Input JSON file containing weight data")
    parser.add_argument("--item", "-n", type=int, help="Only operate on the most recent N records after weight filtering")
    parser.add_argument("--weight", "-w", help="Weight range filter in format a-b (inclusive), e.g. 60-80")
    parser.add_argument("--upload", action="store_true", help="Upload the generated FIT file to Garmin")
    args = parser.parse_args()

    # Load JSON file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File '{input_path}' not found")
        sys.exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            weights = json.load(f)
        
        if not isinstance(weights, list):
            print("❌ Error: JSON should contain a list of weight records")
            sys.exit(1)
        
        print(f"✅ Loaded {len(weights)} weight records from {input_path}")

        # Pre-filter: only keep records where all required fields are present and non-zero
        required_fields = [
            'Date', 'Timestamp', 'Source', 'Weight', 'BMI', 'BodyFat', 'BodyWater',
            'BoneMass', 'MetabolicAge', 'MuscleMass', 'VisceralFat', 'BasalMetabolism', 'BodyScore'
        ]

        def _field_nonzero(rec, field):
            if field not in rec:
                return False
            v = rec.get(field)
            if v is None:
                return False
            # For numeric-like values, consider zero if numeric zero
            try:
                if isinstance(v, bool):
                    return True
                # strings that are numeric
                if isinstance(v, str):
                    s = v.strip()
                    if s == '':
                        return False
                    # if numeric string
                    try:
                        return float(s) != 0.0
                    except Exception:
                        return True
                if isinstance(v, (int, float)):
                    return float(v) != 0.0
            except Exception:
                return False
            return True

        valid_records = []
        for rec in weights:
            ok = True
            if not isinstance(rec, dict):
                continue
            for f in required_fields:
                if not _field_nonzero(rec, f):
                    ok = False
                    break
            if ok:
                valid_records.append(rec)

        print(f"🔎 Valid records after non-zero check: {len(valid_records)} (from {len(weights)})")
        if len(valid_records) == 0:
            print("❌ No valid records to process after non-zero field check.")
            sys.exit(1)

        # use only valid_records for subsequent filtering/sorting
        weights = valid_records

        # Parse weight range if provided (format: a-b)
        weight_range = None
        if args.weight:
            m = re.match(r"^\s*([+-]?\d+(?:\.\d+)?)\s*-\s*([+-]?\d+(?:\.\d+)?)\s*$", args.weight)
            if not m:
                print(f"❌ Error: Invalid --weight format. Use a-b, e.g. 60-80")
                sys.exit(1)
            # Support up to 2 decimal places for weight filtering
            low = round(float(m.group(1)), 2)
            high = round(float(m.group(2)), 2)
            if low > high:
                low, high = high, low
            weight_range = (low, high)

        # Helper to obtain timestamp (seconds) for sorting. Returns None if unavailable.
        def _get_ts(rec):
            if not isinstance(rec, dict):
                return None
            if 'Timestamp' in rec:
                try:
                    return float(rec['Timestamp'])
                except Exception:
                    return None
            if 'Date' in rec:
                dt = rec['Date']
                from datetime import datetime, timezone
                if isinstance(dt, str):
                    # Try common format used elsewhere
                    for fmt in ('%Y-%m-%d %H:%M:%S', "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
                        try:
                            parsed = datetime.strptime(dt, fmt)
                            if parsed.tzinfo is None:
                                parsed = parsed.replace(tzinfo=timezone.utc)
                            return parsed.timestamp()
                        except Exception:
                            continue
                    return None
                if isinstance(dt, datetime):
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt.timestamp()
            return None

        # Apply weight filtering first (priority)
        filtered = []
        if weight_range is not None:
            low, high = weight_range
            for rec in weights:
                try:
                    w = rec.get('Weight')
                except Exception:
                    w = None
                if w is None:
                    continue
                try:
                    wf = round(float(w), 2)
                except Exception:
                    continue
                if wf >= low and wf <= high:
                    filtered.append(rec)
        else:
            filtered = list(weights)

        print(f"🔎 After weight filtering: {len(filtered)} records")

        # Sort by timestamp descending (latest first)
        filtered_with_ts = []
        filtered_no_ts = []
        for rec in filtered:
            ts = _get_ts(rec)
            if ts is None:
                filtered_no_ts.append(rec)
            else:
                filtered_with_ts.append((ts, rec))

        filtered_with_ts.sort(key=lambda x: x[0], reverse=True)
        sorted_filtered = [r for _, r in filtered_with_ts] + filtered_no_ts

        # Apply item limit (most recent N)
        if args.item is not None:
            if args.item <= 0:
                print("❌ Error: --item must be a positive integer")
                sys.exit(1)
            sorted_filtered = sorted_filtered[: args.item]

        print(f"✅ Records selected for conversion: {len(sorted_filtered)}")
        
        # Determine output path with auto-generated filename
        # Extract user ID from input filename (e.g., weight_data_17761239071.json -> 17761239071)
        user_id = ""
        match = re.search(r'(\d+)', input_path.stem)
        if match:
            user_id = match.group(1)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if user_id:
            filename = f"weight_{user_id}_{timestamp}.fit"
        else:
            filename = f"weight_{timestamp}.fit"
        output_path = Path("garmin-fit-filter") / filename
        
        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save filtered JSON alongside FIT
        json_output_path = output_path.with_suffix('.json')
        try:
            with open(json_output_path, 'w', encoding='utf-8') as jf:
                json.dump(sorted_filtered, jf, ensure_ascii=False, indent=2)
            print(f"✅ Wrote filtered JSON: {json_output_path} ({json_output_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"❌ Warning: failed to write filtered JSON - {e}")

        # Convert to FIT
        print(f"🔄 Converting to FIT format...")
        create_weight_fit_file(sorted_filtered, output_path)
        
        print(f"✅ Successfully created FIT file: {output_path}")
        print(f"📊 File size: {output_path.stat().st_size} bytes")
        
        # Upload to Garmin if requested
        if args.upload:
            print(f"🔄 Preparing to upload to Garmin...")
            
            # Load Garmin credentials from users.json
            users_json_path = Path(__file__).parent.parent / "users.json"
            if not users_json_path.exists():
                print(f"❌ Error: users.json not found at {users_json_path}")
                sys.exit(1)
            
            try:
                with open(users_json_path, 'r', encoding='utf-8') as uf:
                    users_config = json.load(uf)
            except Exception as e:
                print(f"❌ Error: Failed to load users.json - {e}")
                sys.exit(1)
            
            users = users_config.get('users', [])
            if not users:
                print(f"❌ Error: No users configured in users.json")
                sys.exit(1)
            
            # Use first user's Garmin credentials
            user = users[0]
            garmin_config = user.get('garmin', {})
            if not garmin_config.get('email') or not garmin_config.get('password'):
                print(f"❌ Error: Garmin credentials not found in users.json")
                sys.exit(1)
            
            email = garmin_config['email']
            password = garmin_config['password']
            domain = garmin_config.get('domain', 'CN')
            
            # Login and upload
            try:
                garmin_client = GarminClient(email, password, auth_domain=domain)
                if not garmin_client.login():
                    print(f"❌ Error: Failed to login to Garmin")
                    sys.exit(1)
                
                upload_result = garmin_client.upload_fit(output_path)
                if upload_result == "SUCCESS":
                    print(f"✅ Successfully uploaded FIT file to Garmin")
                elif upload_result == "DUPLICATE":
                    print(f"⚠️  Warning: Duplicate file detected on Garmin (file may already exist)")
                else:
                    print(f"❌ Error: Upload failed with result: {upload_result}")
                    sys.exit(1)
            except Exception as e:
                print(f"❌ Error: Upload to Garmin failed - {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
        
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
