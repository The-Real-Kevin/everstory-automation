# simple_parser.py
import csv

def parse_single_row(csv_file_path: str, row_index: int = 1):
    """
    Parse a single row and extract all variables
    
    Args:
        csv_file_path: Path to CSV
        row_index: Which row to parse (0-indexed, excluding header)
    """
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if row_index >= len(rows):
            print(f"❌ Row {row_index} does not exist")
            return
        
        row = rows[row_index]
        
        # Extract all variables
        item_name = row.get('Item_Name', '').strip()
        item_name_audio_file_link = row.get('Item_Name_Audio_File_Link', '').strip() or None
        item_description_text = row.get('Item_Description_Text', '').strip()
        item_description_audio_file_link = row.get('Item_Description_Audio_File_Link', '').strip() or None
        date_of_origin_calendar = row.get('Date_Of_Origin_Calendar', '').strip() or None
        date_of_origin_years_ago = int(row.get('Date_Of_Origin_Years_Ago')) if row.get('Date_Of_Origin_Years_Ago', '').strip() else None
        location_of_origin_place_name = row.get('Location_Of_Origin_Place_Name', '').strip() or None
        location_of_origin_gps = row.get('Location_Of_Origin_GPS', '').strip() or None
        item_image_file_link = row.get('Item_Image_File_Link', '').strip() or None
        image_source_link = row.get('Image_Source_Link', '').strip() or None
        image_credit = row.get('Image Credit', '').strip() or None
        next_12 = row.get('Next_12', '').strip() or None
        tags = row.get('Tags', '').strip() or None
        sources = row.get('Sources', '').strip() or None
        
        # Print all variables
        print(f"item_name = '{item_name}'")
        print(f"item_name_audio_file_link = {item_name_audio_file_link}")
        print(f"item_description_text = '{item_description_text[:50]}...'")
        print(f"item_description_audio_file_link = {item_description_audio_file_link}")
        print(f"date_of_origin_calendar = {date_of_origin_calendar}")
        print(f"date_of_origin_years_ago = {date_of_origin_years_ago}")
        print(f"location_of_origin_place_name = {location_of_origin_place_name}")
        print(f"location_of_origin_gps = {location_of_origin_gps}")
        print(f"item_image_file_link = {item_image_file_link}")
        print(f"image_source_link = {image_source_link}")
        print(f"image_credit = {image_credit}")
        print(f"next_12 = {next_12}")
        print(f"tags = {tags}")
        print(f"sources = {sources}")
        
        return {
            'item_name': item_name,
            'item_name_audio_file_link': item_name_audio_file_link,
            'item_description_text': item_description_text,
            'item_description_audio_file_link': item_description_audio_file_link,
            'date_of_origin_calendar': date_of_origin_calendar,
            'date_of_origin_years_ago': date_of_origin_years_ago,
            'location_of_origin_place_name': location_of_origin_place_name,
            'location_of_origin_gps': location_of_origin_gps,
            'item_image_file_link': item_image_file_link,
            'image_source_link': image_source_link,
            'image_credit': image_credit,
            'next_12': next_12,
            'tags': tags,
            'sources': sources
        }

# Usage
if __name__ == "__main__":
    data = parse_single_row('data/moderated_responses_latest.csv', row_index=0)