import json

def format_json(input_file, output_file):
    try:
        with open (input_file, 'r', encoding="utf-8") as f:
            content = f. read()

        # Fix multiple JSON objects in the file (Scenario 1)
        # Attempt to wrap objects in a list if they are not already wrapped
        objects = []
        while content:
            try:
                # Try to load a single JSON object
                obj, idx = json.JSONDecoder().raw_decode(content)
                objects.append(obj)
                content = content[idx:].lstrip()
            except json. JSONDecodeError:
                print ("Error while decoding JSON objects.") 
                break

    # If there were any valid objects, process them into an array and format
        if objects:
            formatted_data = json. dumps (objects, indent = 4)
            with open (output_file, 'w', encoding = "utf-8") as f:
                f.write(formatted_data)
            print ("Formatted JSON written to", output_file)
        else:
            print ("No valid JSON objects found.")
    except FileNotFoundError:
        print("Input file not found.")
    except json.JSONDecodeError as e:
        print("Invalid JSON format in input file:", e)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    input_file = input ("Enter the path to the input JSON file: ")
    output_file = input ("Enter the path to save the formatted JSON file: ")

    format_json(input_file, output_file)

