import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class iot:
    def __init__(self):
        self.df = pd.read_csv("energydata_complete.csv")
        df = self.df
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["time"] = df["date"].dt.strftime("%H:%M")
        df["data"] = df["date"].dt.strftime("%Y-%m-%d")


    def GetDaylyRv1(self,month):
        df = self.df
        if month > "5" or month < "1":
            raise ValueError("Invalid month")
        else:
            df = df[(df["data"] >= f"2016-0{month}-01") & (df["data"] <= f"2016-0{month}-31")]
            df["data"] = df["data"].str.split("-").str[2]
            df["data"] = df["data"].apply(lambda x: x.replace("0", "") if x.startswith("0") else x)
            plt.bar(df["data"], df["rv1"])
            plt.xticks(rotation=90)
            plt.show()

    def GetHourlyWindSpeed(self,month,day):
        df = self.df
        if (month > "5" or month < "1") or (day > "31" or day < "1"):
            raise ValueError("Invalid day")
        else:
            if int(day) < 10:
                day = "0" + str(day)
            df = df[(df["data"] == f"2016-0{month}-{day}")]
            plt.plot(df["time"], df["Windspeed"])
            plt.ylabel("Wind Speed (m/s)")
            plt.xlabel("Time")
            plt.xticks(df["time"][::6],rotation=90)
            plt.show()

    def TemperatureOut(self,typ):
        df = self.df
        typ = int(typ)
        if typ == 1:
            tempout = df.groupby(["month"])["T_out"].mean()
            plt.title("Mean Temperature")
        elif typ == 2:
            tempout = df.groupby(["month"])["T_out"].max()
            plt.title("Max Temperature")
        else:
            tempout = df.groupby(["month"])["T_out"].min()
            plt.title("Min Temperature")

        plt.bar(range(1,6), tempout)
        plt.ylabel("Temperature (C)")
        plt.xlabel("Month")
        plt.show()

    def TempInside(self,month,day):
        if month > "5" or month < "1":
            raise ValueError("Invalid month")
        else:
            if int(day) < 10:
                day = "0" + str(day)

        df = self.df
        Temp = df[df["data"] == f"2016-0{month}-{day}"][["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]]
        time = df[df["data"] == f"2016-0{month}-{day}"]["time"]
        Temp.columns = ["kitchen", "living room", "laundry room", "office room", "bathroom", "outside north",
                        "ironing room", "teenager room", "parents room"]

        plt.plot(time, Temp, label="Temp")
        plt.legend(Temp.columns, loc="upper right",fontsize="small")
        plt.xticks(time[::6], rotation=90)
        plt.show()

    def AvgEnergyConsumption(self):
        df = self.df
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        daily = df[["data", "time", "Appliances"]].copy()
        daily["data"] = pd.to_datetime(daily["data"]).dt.day_name()
        daily["data"] = pd.Categorical(daily["data"], categories=day_order, ordered=True)
        daily = daily.groupby(["time", "data"])["Appliances"].mean()
        daily_matrix = daily.unstack()
        plt.figure(figsize=(12, 8))
        sns.heatmap(daily_matrix, cmap='coolwarm', annot=False)
        plt.title("Average Appliances Energy Consumption by Day and Time")
        plt.xlabel("Day of Week")
        plt.ylabel("Time of Day")
        plt.show()

