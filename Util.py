import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

class iot:
    def __init__(self):
        self.df = pd.read_csv("energydata_complete.csv")
        df = self.df
        df["date"] = pd.to_datetime(df["date"])
        df["time"] = df["date"].dt.strftime("%H:%M")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")


    def GetDaylyRv1(self,month):
        df = self.df
        if month > "5" or month < "1":
            raise ValueError("Invalid month")
        else:
            df = df[(df["date"] >= f"2016-0{month}-01") & (df["date"] <= f"2016-0{month}-31")]
            df["date"] = pd.to_datetime(df["date"])
            plt.bar(df["date"].dt.strftime("%d").str.replace("0",""), df["rv1"])
            plt.show()

    def GetHourlyWindSpeed(self,month,day):
        df = self.df
        if (month > "5" or month < "1") or (day > "31" or day < "0"):
            raise ValueError("Invalid day")
        else:
            if int(day) < 10:
                day = "0" + str(day)
            df = df[(df["date"] == f"2016-0{month}-{day}")]
            plt.plot(df["time"], df["Windspeed"])
            plt.ylabel("Wind Speed (m/s)")
            plt.xlabel("Time")
            plt.xticks(df["time"][::6],rotation=90)
            plt.show()

    def MeanTemperature(self,typ):
        T_out = []
        df = self.df
        df["date"] = pd.to_datetime(df["date"])
        for miesiac in range(1, 6):
            if typ == 1:
                tempout = df[df["date"].dt.strftime("%m") == f"0{miesiac}"]["T_out"].mean()
                plt.title("Mean Temperature")
            elif typ == 2:
                tempout = df[df["date"].dt.strftime("%m") == f"0{miesiac}"]["T_out"].max()
                plt.title("Max Temperature")
            else:
                tempout = df[df["date"].dt.strftime("%m") == f"0{miesiac}"]["T_out"].min()
                plt.title("Min Temperature")
            T_out.append(tempout)
        plt.bar(range(1,6), T_out)
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
        Temp = df[df["date"] == f"2016-0{month}-{day}"][["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9"]]
        time = df[df["date"] == f"2016-0{month}-{day}"]["time"]
        Temp.value_counts()
        Temp.columns = ["kitchen", "living room", "laundry room", "office room", "bathroom", "outside north",
                        "ironing room", "teenager room", "parents room"]

        plt.plot(time, Temp, label="Temp")
        plt.legend(Temp.columns, loc="upper right",fontsize="small")
        plt.xticks(time[::6], rotation=90)
        plt.show()

