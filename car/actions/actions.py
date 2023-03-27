from typing import Any, Text, Dict, List
from rasa_sdk.events import Restarted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
from datetime import datetime
import math
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return [Restarted()]

class ActionManagerlog(Action):
    def name(self) -> Text:
        return "action_managerlog"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno= int(tracker.get_slot('regno'))
        password=tracker.get_slot('password')

        print("regnos",regno)
        print("password",password)

        df = pd.read_csv("files/Manager_dept.csv")
        print(df.head())

        if len(df[(df['ManagerNO'] == regno) & (df['Password']== password)])>0:
            print("successful")
            dept = df[df['ManagerNO'] == regno]["Dept"]
            dept= dept.values[0].split(",")
            print("deptname:", dept)
            buttons = []

            for i in dept:
                buttons.append({"payload": '/' + i + "{" + '"dept"' + ":" + '"' + i + '"' + "}", "title": i})
            print(buttons)
            dispatcher.utter_message(text="Select the department", buttons=buttons,
                                     button_type="vertical")
            return []
        else:
            dispatcher.utter_message(
                text="Username and password is wrong.. Please Enter the correct Username and password ")
            return []

class Actiondept(Action):
    def name(self) -> Text:
        return "action_dept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno = int(tracker.get_slot('regno'))
        password = tracker.get_slot('password')

        print("regnos", regno)
        print("password", password)

        df = pd.read_csv("files/Manager_dept.csv")
        print(df.head())


        if len(df[(df['ManagerNO'] == regno) & (df['Password'] == password)]) > 0:
            subdept= df[df['ManagerNO'] == regno]["SubDept"]
            print("subdeptname:", subdept)
            buttons = []

            for i in subdept:
                buttons.append({"payload": '/' + i + "{" + '"subdept"' + ":" + '"' + i + '"' + "}", "title": i})
            print(buttons)
            dispatcher.utter_message(text="Select the SubDept", buttons=buttons,
                                     button_type="vertical")
            return []
class Actionskill(Action):
    def name(self) -> Text:
        return "action_skill"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno = int(tracker.get_slot('regno'))
        subdept= tracker.get_slot('subdept')

        print("regnos", regno)
        print("subdept", subdept)

        df = pd.read_csv("files/Skills_required.csv")
        print(df.head())
        print("...............",df[df['SubDept'] == subdept]["Technical Skill"].values[0])
        Technical= df[df['SubDept'] == subdept]["Technical Skill"].values[0]

        Problem= df[df['SubDept'] == subdept]["Problem Solving"].values[0]
        creativity= df[df['SubDept'] == subdept]["creativity"].values[0]
        communication= df[df['SubDept'] == subdept]["communication"].values[0]

        dff = pd.read_csv("files/Employee_skill.csv")
        print(df.head())
        emp=dff[(dff["Technical Skill"]>=Technical) & (dff["Problem Solving"]>= Problem) & (dff["creativity"]>= creativity) & (dff["communication"]>= communication)]
        print("emp",emp)
        buttons = []

        for i in list (emp["EmpNo"]):
            buttons.append({"payload": '/' + str(i) + "{" + '"emp"' + ":" + '"' + str(i) + '"' + "}", "title": str(i)})
        print(buttons)
        dispatcher.utter_message(text="Select the employee", buttons=buttons,
                                 button_type="vertical")
        return []

class ActionFinal(Action):
    def name(self) -> Text:
        return "action_final"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # get the location slot
        emp = tracker.get_slot('emp')
        task=tracker.get_slot('task')
        print("this is name", emp)
        df = pd.read_csv("files/Employee_skill.csv")
        df.loc[df["EmpNo"] == emp , ["task assign"]] = task
        df.to_csv("files/Employee_skill.csv",index=False)
        dispatcher.utter_message(f"{task} have assigned successfully")
        return []

class ActionEmptask(Action):
    def name(self) -> Text:
        return "action_emptask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno= tracker.get_slot('employeeno')

        print("regnos",regno)

        df = pd.read_csv("files/Employee_skill.csv")
        print(df.head())
        if len(df[(df['EmpNo'] == regno)])> 0:
            taskassign=df[df['EmpNo'] == regno]["task assign"].values[0]
            print("ta",taskassign)
            if taskassign == 'nan' :
                dispatcher.utter_message(f"Your task is not assign please contact your department head ")
                return []
            else:
                #project= df[df['reg_num'] == regno]["project assigned"].values[0]
                dispatcher.utter_message(f"Your task is to {taskassign} ")
                return []

        else:
            dispatcher.utter_message(text="employee not found.. Please Enter the correct Employee number")
            return []

class ActionStarter(Action):
    def name(self) -> Text:
        return "action_starter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("........heyy............")
        # get the location slot
        regno= tracker.get_slot('employeeno')
        print(regno)
        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        from datetime import date

        today = date.today()

        print("Today's date is:", today)

        df = pd.read_csv("files/Employee_skill.csv")
        print(df.head())
        if len(df[(df['EmpNo'] == regno)])> 0:
            print("@@@@@@@@@@@@@@@@@")
            df = pd.read_csv("files/Employee_skill.csv")
            df.loc[df["EmpNo"] == regno, [str(today)+"_"+"Start time"]] = current_time
            df.to_csv("files/Employee_skill.csv", index=False)
            dispatcher.utter_message(f"Your Working hours has been started")
            return []

class ActionEnder(Action):
    def name(self) -> Text:
        return "action_ender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno= tracker.get_slot('employeeno')

        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        from datetime import date

        today = date.today()

        print("Today's date is:", today)

        df = pd.read_csv("files/Employee_skill.csv")
        print(df.head())
        if len(df[(df['EmpNo'] == regno)])> 0:
            df = pd.read_csv("files/Employee_skill.csv")
            st=df[df['EmpNo'] == regno][str(today)+"_"+"Start time"].values[0]
            df.loc[df["EmpNo"] == regno, [str(today)+"_"+"End time"]] = current_time
            df.loc[df["EmpNo"] == regno, [str(today) + "_" + "Total_hour_worked"]]= datetime.strptime(current_time, "%H:%M:%S")- datetime.strptime(st, "%H:%M:%S")
            df.to_csv("files/Employee_skill.csv", index=False)
            dispatcher.utter_message(f"Your Working hours has been ended")
            return []

class ActionTrackingdetails(Action):
    def name(self) -> Text:
        return "action_trackingdetails"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get the location slot
        regno= tracker.get_slot('employeeno')



        df = pd.read_csv("files/Employee_skill.csv")
        print(df.head())
        if len(df[(df['EmpNo'] == regno)])> 0:
            df = pd.read_csv("files/Employee_skill.csv")
            li=[col for col in df if col.endswith('Total_hour_worked')]
            hours=list(df[df['EmpNo'] == regno][li].values)
            date=[col.split("_")[0] for col in li]
            res={"Date":date,"Hours":hours[0].tolist()}
            print("result",res)

            dispatcher.utter_message(f"{res}")
            return []
