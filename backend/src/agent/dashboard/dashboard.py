import json

final_dashboard = []

def create_graph(data, args):

    for metric, values in data.items():

        title = f"{args["coin_id"].capitalize()} {metric.capitalize()}"
        subtitle = f"From {values[0][0]} to {values[-1][0]}."
        parsed_data = []

        for point in values:
            parsed_data.append({
                "date": point[0],
                "line": point[1]
            })

        final_dashboard.append({
            "type": "graph",
            "title": title,
            "subtitle": subtitle,
            "data": parsed_data
        })

table_coins = []
current_table_headers = []
current_table_data = []

def create_table(data, args):

    data = data[0]

    row = []
    row.append(args["coin_id"].capitalize())
    table_coins.append(args["coin_id"].capitalize())

    for metric, value in data.items():
        if metric not in ["image", "roi"]:
            if ",".join([word.capitalize() for word in metric.split("_")]) not in current_table_headers:
                current_table_headers.append(" ".join([word.capitalize() for word in metric.split("_")]))
            if type(value) == int or type(value) == float:
                row.append(f"{value:,.2f}" if value else "Unknown")
            else:
                row.append(value if value else "Unknown")
    
    current_table_data.append(row)
            
    
def finalize_table():
    final_dashboard.append({
        "type": "table",
        "title": ", ".join(table_coins) + " Metrics",
        "subtitle": f"Various data points for {", ".join(table_coins)}.",
        "headers": current_table_headers,
        "data": current_table_data
    })
    print(json.dumps({
        "type": "table",
        "title": " ".join(table_coins),
        "subtitle": f"Various data for {", ".join(table_coins)}.",
        "headers": current_table_headers,
        "data": current_table_data
    }, indent=2))


def create_radial(data, args):
    pass

def create_reccomended(data):
    pass