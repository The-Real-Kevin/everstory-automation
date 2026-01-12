# parse_moderated_responses.py
import csv
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModeratedResponseItem:
    """
    Data class representing a single row from the Moderated Responses sheet
    """
    # Basic item info
    item_name: str
    item_name_audio_file_link: Optional[str]
    item_description_text: str
    item_description_audio_file_link: Optional[str]
    
    # Date information
    date_of_origin_calendar: Optional[str]
    date_of_origin_years_ago: Optional[int]
    
    # Location information
    location_of_origin_place_name: Optional[str]
    location_of_origin_gps: Optional[str]
    
    # Media files
    item_image_file_link: Optional[str]
    image_source_link: Optional[str]
    image_credit: Optional[str]
    
    # Metadata
    next_12: Optional[str]
    tags: Optional[str]
    sources: Optional[str]
    
    def __repr__(self):
        return f"ModeratedResponseItem(item_name='{self.item_name}')"

def parse_int_or_none(value: str) -> Optional[int]:
    """Parse string to int, return None if empty or invalid"""
    if not value or value.strip() == '':
        return None
    try:
        return int(value)
    except ValueError:
        return None

def parse_str_or_none(value: str) -> Optional[str]:
    """Return string or None if empty"""
    if not value or value.strip() == '':
        return None
    return value.strip()

def parse_moderated_responses(csv_file_path: str) -> List[ModeratedResponseItem]:
    """
    Parse the Moderated Responses CSV file into structured data
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        List of ModeratedResponseItem objects
    """
    items = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (row 1 is header)
            try:
                # Parse each column with proper type conversion
                item = ModeratedResponseItem(
                    # Basic info (required)
                    item_name=row.get('Item_Name', '').strip(),
                    item_name_audio_file_link=parse_str_or_none(row.get('Item_Name_Audio_File_Link')),
                    item_description_text=row.get('Item_Description_Text', '').strip(),
                    item_description_audio_file_link=parse_str_or_none(row.get('Item_Description_Audio_File_Link')),
                    
                    # Date info
                    date_of_origin_calendar=parse_str_or_none(row.get('Date_Of_Origin_Calendar')),
                    date_of_origin_years_ago=parse_int_or_none(row.get('Date_Of_Origin_Years_Ago')),
                    
                    # Location info
                    location_of_origin_place_name=parse_str_or_none(row.get('Location_Of_Origin_Place_Name')),
                    location_of_origin_gps=parse_str_or_none(row.get('Location_Of_Origin_GPS')),
                    
                    # Media
                    item_image_file_link=parse_str_or_none(row.get('Item_Image_File_Link')),
                    image_source_link=parse_str_or_none(row.get('Image_Source_Link')),
                    image_credit=parse_str_or_none(row.get('Image Credit')),
                    
                    # Metadata
                    next_12=parse_str_or_none(row.get('Next_12')),
                    tags=parse_str_or_none(row.get('Tags')),
                    sources=parse_str_or_none(row.get('Sources'))
                )
                
                # Validate required fields
                if not item.item_name:
                    print(f"⚠️  Row {row_num}: Skipping - missing Item_Name")
                    continue
                
                if not item.item_description_text:
                    print(f"⚠️  Row {row_num}: Skipping - missing Item_Description_Text")
                    continue
                
                items.append(item)
                
            except Exception as e:
                print(f"❌ Error parsing row {row_num}: {e}")
                continue
    
    return items

def print_item_summary(item: ModeratedResponseItem):
    """Print a nice summary of a parsed item"""
    print("=" * 70)
    print(f"📦 Item: {item.item_name}")
    print("=" * 70)
    print(f"Description: {item.item_description_text[:100]}...")
    
    if item.location_of_origin_place_name:
        print(f"📍 Location: {item.location_of_origin_place_name}")
        if item.location_of_origin_gps:
            print(f"   GPS: {item.location_of_origin_gps}")
    
    if item.date_of_origin_calendar:
        print(f"📅 Date: {item.date_of_origin_calendar}")
    elif item.date_of_origin_years_ago:
        print(f"📅 Date: {item.date_of_origin_years_ago} years ago")
    
    print(f"\n🎵 Audio Files:")
    print(f"   Name: {'✅' if item.item_name_audio_file_link else '❌'}")
    print(f"   Description: {'✅' if item.item_description_audio_file_link else '❌'}")
    
    print(f"\n🖼️  Image: {'✅' if item.item_image_file_link else '❌'}")
    
    if item.tags:
        print(f"\n🏷️  Tags: {item.tags[:50]}...")
    
    print()

def convert_to_supabase_params(item: ModeratedResponseItem) -> Dict:
    """
    Convert a ModeratedResponseItem to parameters for the Supabase insert_new_item function
    
    Note: This assumes media files have already been uploaded to Supabase Storage
    and returns the parameters structure without s3_keys (you'll need to add those)
    """
    return {
        # Required
        'p_item_name': item.item_name,
        'p_item_description_text': item.item_description_text,
        
        # Optional - basic
        'p_default_language': 'en',
        'p_created_by': None,  # Will use auth.uid()
        
        # Optional - location
        'p_location_name': item.location_of_origin_place_name,
        'p_location_gps': item.location_of_origin_gps,
        'p_loc_type': 'country',  # You may need logic to determine this
        
        # Optional - date
        'p_date_calendar': item.date_of_origin_calendar,
        'p_years_ago': item.date_of_origin_years_ago,
        
        # Optional - media (s3_keys - you need to upload files first)
        'p_name_audio_s3_key': None,  # TODO: Upload and set
        'p_description_audio_s3_key': None,  # TODO: Upload and set
        'p_image_s3_key': None,  # TODO: Upload and set
        
        # Optional - metadata
        'p_tags': item.tags,
        'p_sources': item.sources,
        'p_image_credit': item.image_credit,
        
        # Optional - status
        'p_review_status': 'approved'  # Since it's from "Moderated Responses"
    }

def main():
    """Main function to test parsing"""
    csv_file = 'data/moderated_responses_latest.csv'
    
    print("🔍 Parsing Moderated Responses...")
    items = parse_moderated_responses(csv_file)
    
    print(f"\n✅ Successfully parsed {len(items)} items\n")
    
    # Show first 3 items
    for i, item in enumerate(items[:3], 1):
        print_item_summary(item)
    
    if len(items) > 3:
        print(f"... and {len(items) - 3} more items")
    
    # Show how to convert to Supabase params
    if items:
        print("\n" + "=" * 70)
        print("📤 Example: Supabase Parameters for First Item")
        print("=" * 70)
        params = convert_to_supabase_params(items[0])
        import json
        print(json.dumps(params, indent=2))

if __name__ == "__main__":
    main()