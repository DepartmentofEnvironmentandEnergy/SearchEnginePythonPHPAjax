import json
import re

# read in malformed json
try:
    with open('website_data.json') as f:
        malformed = f.read()
except FileNotFoundError:
    print("File not found.")
else:
    # add double quotes around all keys
    fixed = malformed.replace("'", '"')
    fixed = fixed.replace(':{', ':{ "')

    # replace all double quotes around values with single quotes
    fixed = fixed.replace(': "', ': \'')
    fixed = fixed.replace('",', '\',')
    fixed = fixed.replace('"}', '"\'}')

    # remove any trailing commas after last value in an object or array
    fixed = re.sub(r',\s*([}\]])', r'\1', fixed)

    # parse and re-serialize the fixed json
    try:
        parsed = json.loads(fixed)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e.msg} at line {e.lineno}, column {e.colno}")
    else:
        fixed = json.dumps(parsed, indent=4)

        # write fixed json to file
        with open('fixed.json', 'w') as f:
            f.write(fixed)
