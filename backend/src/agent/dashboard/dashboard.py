import json

class DashboardBuilder:

    def __init__(self):
        self.table_coins = []
        self.final_dashboard = []
        self.current_table_headers = []
        self.current_table_data = []
        self.recommended = []

    def create_graph(self, data, args):
        for metric, values in data.items():

            title = f"{args['coin_id'].capitalize()} {metric.capitalize()}"
            subtitle = f"From {values[0][0]} to {values[-1][0]}."
            parsed_data = []

            for point in values:
                parsed_data.append({
                    "date": point[0],
                    "line": point[1]
                })

            self.final_dashboard.append({
                "type": "graph",
                "title": title,
                "subtitle": subtitle,
                "data": parsed_data,
                "cols": 2
            })

    def create_table(self, data, args):

        data = data[0]

        row = []
        row.append(args["coin_id"].capitalize())
        self.table_coins.append(args["coin_id"].capitalize())

        for metric, value in data.items():
            if metric not in ["image", "roi"]:
                if ",".join([word.capitalize() for word in metric.split("_")]) not in self.current_table_headers:
                    self.current_table_headers.append(" ".join([word.capitalize() for word in metric.split("_")]))
                if type(value) == int or type(value) == float:
                    row.append(f"{value:,.2f}" if value else "Unknown")
                else:
                    row.append(value if value else "Unknown")
        
        self.current_table_data.append(row)

    
    def finalize_table(self):
        if len(self.current_table_headers) > 0:
            self.final_dashboard.append({
                "type": "table",
                "title": ", ".join(self.table_coins) + " Metrics",
                "subtitle": f"Various data points for {', '.join(self.table_coins)}.",
                "headers": self.current_table_headers,
                "data": self.current_table_data,
                "cols": 1
            })

    
    def create_radial(self, data, args, type_):

        if data[-1].get("average_sentiments", None):
            title = f"{type_} for {args['coin'].capitalize() if args.get("coin", None) else ' the overall market.'}"
            subtitle = f"{type_} calulated using various posts from the past {args['time_period']}."
            value = data[-1]["average_sentiments"]["overall_average_sentiment"]
            self.final_dashboard.append({
                "type": "radial",
                "title": title,
                "subtitle": subtitle,
                "min": -1,
                "max": 1,
                "value": round(value, 2),
                "label": "Negative" if value < 0 else "Positive",
                "leftLabel": "Positive",
                "rightLabel": "Negative",
                "cols": 1,
                "color": "red" if value < 0 else "green"
            })

        else:
            title = f"Fear and Greed"
            subtitle = f"The emotional state of the market from the past {args['limit']} days."
            value = sum([int(item["value"]) for item in data]) / len(data)
            self.final_dashboard.append({
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

    
    def create_recomended(self, data):
        for article in data:
            self.recommended.append({
                "url": article["url"],
                "content": article["content"],
                "title": article["title"]
            })

    
    def finalize_recommended(self):
        if len(self.recommended) > 0:
            self.final_dashboard.append({
                "type": "recommended",
                "recommended": self.recommended,
                "cols": 2
            })

    
    def add_summary(self, summary):
        self.final_dashboard.append({
            "type": "summary",
            "title": "Summary",
            "subtitle": "A summary of all the collected data.",
            "text": summary,
            "cols": 2
        })

    
    def sort_dashboard(self):

        ones = [d for d in self.final_dashboard if d["cols"] == 1]
        twos = [d for d in self.final_dashboard if d["cols"] == 2]

        pattern = ["1", "2", "2", "1"]
        result = []
        i = 0

        while ones or twos:
            step = pattern[i % len(pattern)]

            if step == "1" and ones:
                result.append(ones.pop(0))
            elif step == "2" and twos:
                result.append(twos.pop(0))
            else:
                if ones:
                    result.append(ones.pop(0))
                elif twos:
                    result.append(twos.pop(0))

            i += 1

        self.final_dashboard = result

    
    def get_final_dashboard(self):
        return self.final_dashboard