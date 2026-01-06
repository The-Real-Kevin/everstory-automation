# compare_sheets.py
import csv
import os
import sys
from datetime import datetime

def read_csv(filepath):
    """Read CSV file and return list of rows"""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    print(f"📄 Read {len(data)} rows from {filepath}")
    return data

def rows_to_set(rows, skip_header=True):
    """
    Convert rows to a set of tuples for comparison
    Skip header row by default
    """
    start_idx = 1 if skip_header else 0
    row_set = set()
    
    for row in rows[start_idx:]:
        # Convert row to tuple (lists aren't hashable, tuples are)
        row_tuple = tuple(row)
        row_set.add(row_tuple)
    
    return row_set

def find_new_rows(current_file, previous_file, output_file='data/new_rows.csv'):
    """
    Compare current and previous CSV files
    Find rows that exist in current but not in previous
    Save new rows to output file
    """
    
    print("=" * 70)
    print("🔍 Starting comparison...")
    print("=" * 70)
    
    # Read both files
    current_data = read_csv(current_file)
    previous_data = read_csv(previous_file)
    
    # Handle missing files
    if current_data is None:
        print("❌ Current file not found!")
        return []
    
    if previous_data is None:
        print("⚠️  Previous file not found - treating all rows as new")
        new_rows = current_data[1:]  # All rows except header are "new"
        header = current_data[0] if current_data else []
    else:
        # Extract headers (should be the same)
        header = current_data[0] if current_data else []
        
        # Convert to sets for comparison
        current_set = rows_to_set(current_data)
        previous_set = rows_to_set(previous_data)
        
        # Find new rows (in current but not in previous)
        new_row_tuples = current_set - previous_set
        
        # Convert back to lists
        new_rows = [list(row) for row in new_row_tuples]
    
    # Print summary
    print(f"\n📊 Comparison Summary:")
    print(f"   Current file rows:  {len(current_data) - 1 if current_data else 0}")
    print(f"   Previous file rows: {len(previous_data) - 1 if previous_data else 0}")
    print(f"   🆕 New rows found:  {len(new_rows)}")
    
    # Save new rows to file
    if new_rows:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(header)
            # Write new rows
            writer.writerows(new_rows)
        
        print(f"\n✅ Saved {len(new_rows)} new rows to {output_file}")
        
        # Show preview of new rows
        print(f"\n👀 Preview of new rows:")
        for i, row in enumerate(new_rows[:3], 1):  # Show first 3
            # Show first 3 columns of each row
            preview = row[:3] if len(row) >= 3 else row
            print(f"   Row {i}: {preview}...")
        
        if len(new_rows) > 3:
            print(f"   ... and {len(new_rows) - 3} more rows")
    else:
        print("\n✅ No new rows found - sheets are identical")
    
    print("=" * 70)
    
    return new_rows

def main():
    """Main function"""
    
    # File paths
    current_file = 'data/moderated_responses_latest.csv'
    previous_file = 'data/moderated_responses_previous.csv'
    output_file = 'data/new_rows.csv'
    
    # Check if files exist
    if not os.path.exists(current_file):
        print(f"❌ Error: Current file not found: {current_file}")
        sys.exit(1)
    
    # Find new rows
    new_rows = find_new_rows(current_file, previous_file, output_file)
    
    # Return exit code based on whether new rows were found
    if new_rows:
        print(f"\n🎉 Found {len(new_rows)} new rows!")
        sys.exit(0)  # Success
    else:
        print(f"\n💤 No new rows found")
        sys.exit(0)  # Still success, just no changes

if __name__ == "__main__":
    main()
