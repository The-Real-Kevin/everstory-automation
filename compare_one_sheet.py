# compare_sheets_advanced.py
import csv
import os
import sys
import json
from datetime import datetime

def read_csv(filepath):
    """Read CSV file and return list of rows"""
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    return data

def create_row_hash(row):
    """
    Create a unique hash for a row based on key columns
    This is more reliable than comparing entire rows
    """
    # Use first few columns as identifier (adjust as needed)
    # For example: Timestamp + Item_Name + Description
    key_columns = row[:5] if len(row) >= 5 else row
    return tuple(key_columns)

def find_new_rows_with_order(current_file, previous_file, output_file='data/new_rows.csv'):
    """
    Find new rows while preserving order
    Also handles duplicate detection more intelligently
    """
    
    print("=" * 70)
    print("🔍 Comparing Sheets: Moderated Responses")
    print("=" * 70)
    
    # Read files
    current_data = read_csv(current_file)
    previous_data = read_csv(previous_file)
    
    if current_data is None:
        print("❌ Current file not found!")
        return []
    
    if not current_data:
        print("⚠️  Current file is empty!")
        return []
    
    header = current_data[0]
    current_rows = current_data[1:]
    
    # If no previous file, all rows are new
    if previous_data is None or len(previous_data) <= 1:
        print("⚠️  No previous data - all rows are considered new")
        new_rows = current_rows
    else:
        previous_rows = previous_data[1:]
        
        # Create set of previous row hashes
        previous_hashes = {create_row_hash(row) for row in previous_rows}
        
        # Find new rows (preserve order)
        new_rows = []
        for row in current_rows:
            row_hash = create_row_hash(row)
            if row_hash not in previous_hashes:
                new_rows.append(row)
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   Current rows:      {len(current_rows)}")
    print(f"   Previous rows:     {len(previous_data[1:]) if previous_data and len(previous_data) > 1 else 0}")
    print(f"   🆕 New rows:       {len(new_rows)}")
    
    # Save new rows
    if new_rows:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(new_rows)
        
        print(f"\n✅ Saved {len(new_rows)} new rows to {output_file}")
        
        # Preview
        print(f"\n👀 Preview of new rows:")
        for i, row in enumerate(new_rows[:5], 1):
            # Show key columns
            preview = [row[j] if j < len(row) else '' for j in [0, 1, 3]]  # Verification, Moderator, Item_Name
            print(f"   {i}. {preview}")
        
        if len(new_rows) > 5:
            print(f"   ... and {len(new_rows) - 5} more")
        
        # Save metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'total_new_rows': len(new_rows),
            'current_total': len(current_rows),
            'previous_total': len(previous_data[1:]) if previous_data and len(previous_data) > 1 else 0
        }
        
        with open('data/comparison_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n📝 Metadata saved to data/comparison_metadata.json")
    else:
        print("\n✅ No new rows - sheets are identical")
    
    print("=" * 70)
    
    return new_rows

def filter_verified_rows(rows, verification_column_index=0):
    """
    Filter to only keep rows where verification column == 'verified'
    """
    verified_rows = []
    
    for row in rows:
        if len(row) > verification_column_index:
            if row[verification_column_index].lower() == 'verified':
                verified_rows.append(row)
    
    return verified_rows

def main():
    """Main function"""
    
    current_file = 'data/moderated_responses_latest.csv'
    previous_file = 'data/moderated_responses_previous.csv'
    output_file = 'data/new_rows.csv'
    verified_output = 'data/new_verified_rows.csv'
    
    # Find new rows
    new_rows = find_new_rows_with_order(current_file, previous_file, output_file)
    
    # Filter for verified rows only
    if new_rows:
        verified_rows = filter_verified_rows(new_rows)
        
        if verified_rows:
            print(f"\n🔐 Found {len(verified_rows)} verified rows out of {len(new_rows)} new rows")
            
            # Save verified rows separately
            current_data = read_csv(current_file)
            header = current_data[0] if current_data else []
            
            with open(verified_output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(verified_rows)
            
            print(f"✅ Saved verified rows to {verified_output}")
        else:
            print(f"\n⚠️  No verified rows found among new rows")
    
    print("\n✨ Comparison complete!")

if __name__ == "__main__":
    main()