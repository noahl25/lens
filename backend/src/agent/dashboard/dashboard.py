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
            "data": parsed_data,
            "cols": 2
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
    if len(current_table_headers) > 0:
        final_dashboard.append({
            "type": "table",
            "title": ", ".join(table_coins) + " Metrics",
            "subtitle": f"Various data points for {", ".join(table_coins)}.",
            "headers": current_table_headers,
            "data": current_table_data,
            "cols": 1
        })


def create_radial(data, args, type_):
    

    if data[-1].get("average_sentiments", None):
        title = f"{type_} for {args["coin"].capitalize() if args["coin"] else " the overall market."}"
        subtitle = f"{type_} calulated using various posts from the past {args["time_period"]}."
        value = data[-1]["average_sentiments"]["overall_average_sentiment"]
        final_dashboard.append({
            "type": "radial",
            "title": title,
            "subtitle": subtitle,
            "min": -1,
            "max": 1,
            "value": value,
            "label": "Negative" if value < 0 else "Positive",
            "leftLabel": "Positive",
            "rightLabel": "Negative",
            "cols": 1,
            "color": "red" if value < 0 else "green"
        })

    else:
        title = f"Fear and Greed"
        subtitle = f"The emotional state of the market from the past {args["limit"]} days."
        value = sum([int(item["value"]) for item in data]) / len(data)
        final_dashboard.append({
            "type": "radial",
            "title": title,
            "subtitle": subtitle,
            "min": 0,
            "max": 100,
            "value": round(value, 2),
            "label": "Fear" if value < 50 else "Greed",
            "leftLabel": "Greed",
            "rightLabel": "Fear",
            "cols": 1,
            "color": "red" if value < 50 else "green"
        })
        

recommended = []
def create_recomended(data):
    for article in data:
        recommended.append({
            "url": article["url"],
            "content": article["content"],
            "title": article["title"]
        })

def finalize_recommended():
    if len(recommended) > 0:
        final_dashboard.append({
            "type": "recommended",
            "recommended": recommended,
            "cols": 2
        })

def add_summary(summary):
    final_dashboard.append({
        "type": "summary",
        "title": "Summary",
        "subtitle": "A summary of all the collected data.",
        "text": summary,
        "cols": 2
    })

def sort_dashboard():
    
    global final_dashboard
    ones = [d for d in final_dashboard if d["cols"] == 1]
    twos = [d for d in final_dashboard if d["cols"] == 2]

    result = []
    while ones or twos:
        if ones:
            result.append(ones.pop(0))
        if twos:
            result.append(twos.pop(0))

    graphs = [d for d in result if d.get("type") == "graph"]
    if graphs:
        non_graphs = [d for d in result if d.get("type") != "graph"]
        result = graphs + non_graphs

    final_dashboard = result