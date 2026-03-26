from Util import iot
from decide import datarange

iot_data = iot()
datarange = datarange()
while True:
    try:

        print("1. Daily RV1\n"
              "2. Hourly Wind Speed\n"
              "3. Temperature out\n"
              "4. Temperature inside\n"
              "5. Average Energy Consumption\n"
              "Type 'exit' to quit\n")
        decide = input("Choose one of the options: ")

        if decide == "1":
            datarange.collect_data(1)
            iot_data.GetDaylyRv1(datarange.month)
        elif decide == "2":
            datarange.collect_data(2)
            iot_data.GetHourlyWindSpeed(datarange.month, datarange.day)
            print(datarange.month, datarange.day)
        elif decide == "3":
            datarange.collect_data(3)
            iot_data.TemperatureOut(datarange.datatype)
        elif decide == "4":
            datarange.collect_data(4)
            iot_data.TempInside(datarange.month, datarange.day)
        elif decide == "5":
            iot_data.AvgEnergyConsumption()
        elif decide.lower() == "exit":
            break
        else:
            print(f"There is no option nr: {decide} ")
    except ValueError:
        print("Error with date")

