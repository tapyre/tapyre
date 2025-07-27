import sys
import subprocess
import json

data_list = [
    {
        "id": 1,
        "name": "Alice Smith",
    },
    {
        "id": 2,
        "name": "Bob Johnson",
    },
    {
        "id": 3,
        "name": "Charlie Brown",
    },
    {
        "id": 4,
        "name": "Diana Prince",
    },
    {
        "id": 5,
        "name": "Edward Nigma",
    },
    {
        "id": 6,
        "name": "Fiona Glenanne",
    },
]


def main():
    try:
        input_data = sys.stdin.read()

        query = json.loads(input_data)
        mode = query.get("mode", "").lower()
        text = query.get("text", "").lower()

        if text:
            filtered_list = [item for item in data_list if text in item["name"].lower()]
        else:
            filtered_list = data_list

        result = {}

        if mode == "search":
            result = {
                "type": "list",
                "data": filtered_list,
            }
        elif mode == "launch":
            subprocess.run(["notify-send", text])

        sys.stdout.write(json.dumps(result, indent=4))

    except json.JSONDecodeError:
        sys.stderr.write("Error: Invalid JSON received.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
