import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class iot:
    def __init__(self):
        self.df = pd.read_csv("energydata_complete.csv")
        df = self.df
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["time"] = df["date"].dt.strftime("%H:%M")
        df["data"] = df["date"].dt.strftime("%Y-%m-%d")


    def GetDaylyPressure(self,month):
        df = self.df
        if month > "5" or month < "1":
            raise ValueError("Invalid month")
        else:

            df = df[(df["data"] >= f"2016-0{month}-01") & (df["data"] <= f"2016-0{month}-31")]
            df["day"] = df["data"].str.split("-").str[2]

            daily_pressure = df.groupby("day")["Press_mm_hg"].mean()

            plt.bar(daily_pressure.index, daily_pressure.values)
            plt.xticks(rotation=90)
            plt.ylabel("Pressure (mm Hg)")
            plt.xlabel("Day of month")
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

    def TemperatureOut(self):
        df = self.df
        df["month"] = df["date"].dt.month_name()
        df = df.groupby(["month", "day"])["T_out"].mean().reset_index()
        month_order = ["January", "February", "March", "April", "May"]
        df["month"] = pd.Categorical(df["month"], month_order, ordered=True)
        df = df.sort_values("month")
        df = df.set_index(["month"])

        print(df.head)

        df.boxplot(by='month', column="T_out")

        for i, month in enumerate(df.index.unique(), start=1):
            y = df.loc[month]["T_out"]
            plt.scatter([i] * len(y), y, alpha=0.3)
        plt.ylabel("Temperature (C)")
        plt.xlabel("Month")
        plt.suptitle("")
        plt.title("Monthly Temperature Data")
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

