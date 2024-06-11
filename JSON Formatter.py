import json
import re
from datetime import datetime, timezone

def parse_asc_x12_message(asc_x12_message):
    if not asc_x12_message:
        return {}
    
    segments = re.findall(r'([A-Z]{2})(\|[^~]+)~?', asc_x12_message)
    parsed_message = {}
    for seg_id, seg_data in segments:
        fields = seg_data.split('|')[1:]  # Exclude the segment ID
        if seg_id not in parsed_message:
            parsed_message[seg_id] = []
        parsed_message[seg_id].append(fields)
    return parsed_message

def generate_fhir_resources(parsed_message):
    resources = []

    # Generate Patient resource
    if 'NM1' in parsed_message:
        patient_resource = {
            "resourceType": "Patient",
            "id": "example",
            "meta": {
                "versionId": "1",
                "lastUpdated": datetime.now(timezone.utc).isoformat()
            },
            "identifier": {
                "system": "http://example.org/patient_id",
                "value": parsed_message['NM1'][0][8]
            },
            "name": {
                "use": "official",
                "family": parsed_message['NM1'][0][3],
                "given": [parsed_message['NM1'][0][4]]
            },
            "gender": parsed_message['NM1'][0][5]
        }
        resources.append(patient_resource)

    # Add more resources as needed

    return resources

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)

def get_input_filename():
    return input("Enter the location of the input ASC X12 message file: ")

def get_output_filename():
    return input("Enter the location where you want to save the output FHIR JSON file: ")

# Example usage
if __name__ == "__main__":
    input_asc_x12_file = get_input_filename()
    output_fhir_json_file = get_output_filename()

    # Read ASC X12 message from file
    with open(input_asc_x12_file, 'r') as file:
        asc_x12_message = file.read()

    # Parse ASC X12 message
    asc_x12_parsed = parse_asc_x12_message(asc_x12_message)

    # Check if parsing was successful
    if not asc_x12_parsed:
        print("Error: Unable to parse ASC X12 message.")
    else:
        # Generate FHIR resources
        fhir_resources = generate_fhir_resources(asc_x12_parsed)

        # Save FHIR resources to file
        save_json_to_file(fhir_resources, output_fhir_json_file)
