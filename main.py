from datetime import datetime, timedelta

file_path = "alert.txt"
output_file = "formatted_alert_data.txt"

formattedData = {}

def convertTime(time):
    utc_format = "%Y-%m-%d %H:%M"
    pdt_time = (datetime.strptime(time, utc_format) - timedelta(hours=8)).strftime(utc_format)
    return pdt_time

def format():
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            items = line.split()
            if len(items) == 6:
                ip_address = items[0]
                port = items[1]
                service = items[2]
                category = items[3]
                date = items[4]
                time = items[5]

                # Convert the time to PDT
                date_pdt = convertTime(date + " " + time)

                if ip_address in formattedData:
                    # If IP is already in the dictionary, append the data
                    formattedData[ip_address]['ports'].append(port)
                    formattedData[ip_address]['dates'].add(date + " " + time)
                    formattedData[ip_address]['dates_pdt'].add(date_pdt)

                    # Add the service and category to the list if they are not already in the set
                    if service not in formattedData[ip_address]['services_set']:
                        formattedData[ip_address]['services'].append(service)
                        formattedData[ip_address]['services_set'].add(service)

                    if category not in formattedData[ip_address]['categories_set']:
                        formattedData[ip_address]['categories'].append(category)
                        formattedData[ip_address]['categories_set'].add(category)
                else:
                    # If IP is not in the dictionary, add it and initialize the data
                    formattedData[ip_address] = {
                        'ports': [port],
                        'services': [service],
                        'categories': [category],
                        'dates': {date + " " + time},
                        'dates_pdt': {date_pdt},
                        'services_set': {service},
                        'categories_set': {category}
                    }

format()

# Save the data to a single text file with the specified format
with open(output_file, "w") as output:
    for ip, data in formattedData.items():
        ip_str = ip
        time_str = ', '.join(data['dates'])
        date_pdt = ', '.join(data['dates_pdt'])
        port_str = ', '.join(data['ports'])
        service_str = ', '.join(data['services'])
        category_str = ', '.join(data['categories'])
        output.write(f"{ip_str}\t\t\t\t{time_str}\t{date_pdt}\t{port_str}\t{service_str}\t{category_str}\n")

print(f"Formatted data saved to {output_file}")
