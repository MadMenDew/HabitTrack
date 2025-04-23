from abc import ABC, abstractmethod

#  STRATEGY PATTERN

#Checks different progress checking styles
class ProgressStrategy(ABC):
    @abstractmethod
    def check_progress(self, completions):
        pass

#Strict strategy checks that ALL habit completions are true -- perfect streak
class StrictStrategy(ProgressStrategy):
    def check_progress(self, completions):
        return all(completions)

#Flexible strategy checks that habit was completed 70% of the time
class FlexibleStrategy(ProgressStrategy):
    def check_progress(self, completions):
        return (sum(completions) / len(completions)) >= 0.7
    

# This is the base habit class all habit tupes inheret from
class Habit(ABC):
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.completions = [] #stores true/false for each completion
        
    @abstractmethod
    def complete(self, status):
        pass

    #evaluate how the user is doing based on their chosen strategy
    def evaluate_progress(self):
        return self.strategy.check_progress(self.completions)
        
        #A daily habit - used for things you want to do every day
class DailyHabit(Habit):
    def complete(self, status):
        print(f"Daily habit '{self.name}' done: {status}")
        self.completions.append(status)

        #A weekly habit - used for things done once a week
class WeeklyHabit(Habit):
    def complete(self, status):
        print(f"Weekly habit '{self.name}' done: {status}")
        self.completions.append(status)


# FACTORY METHOD PATTERN

#This class creates different habit types based on input 
class HabitFactory:
    @staticmethod
    def create_habit(habit_type, name, strategy):
        if habit_type == "daily":
            return DailyHabit(name, strategy)
        elif habit_type == "weekly":
            return WeeklyHabit(name, strategy)
        else:
            raise ValueError("Unknown habit type")

# DECORATOR PATTERN

# Base decorator - wraps a habit and forwards method calls
class HabitDecorator(Habit):
    def __init__(self, habit):
        super().__init__(habit.name, habit.strategy)
        self._habit = habit
    
    def complete(self, status):
        self._habit.complete(status)

    def evaluate_progress(self):
        return self._habit.evaluate_progress()
    
#adds a reminder message before completing the habit
class ReminderHabit(HabitDecorator):
    def complete(self, status):
        print("Reminder: Don't forget your habit!")
        super().complete(status)

# Adds a reward message after completing the habit
class RewardHabit(HabitDecorator):
    def complete(self, status):
        super().complete(status)
        if status:
            print("Good job! You get points!")

# Test Run

if __name__ == "__main__":
    
    name = input("What is the name of your habit: ")
    frequency = input("Is this a daily or weekly task (enter 'D' for daily or 'W' for weekly): ")
    if frequency.lower() == 'd':
        frequency = "daily"
    elif frequency.lower() == 'w':
        frequency = 'weekly'
    else:
        print("Invalid frequency. Defaulting to daily.")
        frequency = "daily"

    strategy = input("Is this a strict or flexible task (enter 'S' for strict or 'F' for flexible): ")
    if strategy.lower() == 's':
        strategy = StrictStrategy()
    elif strategy.lower() == 'f':
        strategy = FlexibleStrategy()
    else:
        print("Invalid entry. Defaulting to flexible")
        strategy = FlexibleStrategy()

    habit = HabitFactory.create_habit(frequency, name, strategy)

    habit = ReminderHabit(habit)
    habit = RewardHabit(habit)

    day1 = input("Did you complete the habit on day 1 (enter 'Y' for yes, 'N' for no): ")
    if day1.lower() == 'y':
        day1= True
    elif day1.lower() == 'n':
        day1= False
    else:
        print("Invalid entry. Defaulting to no.")
        day1=False
    
    day2 = input("Did you complete the habit on day 1 (enter 'Y' for yes, 'N' for no): ")
    if day2.lower() == 'y':
        day2= True
    elif day2.lower() == 'n':
        day2= False
    else:
        print("Invalid entry. Defaulting to no.")
        day2=False

    day3 = input("Did you complete the habit on day 1 (enter 'Y' for yes, 'N' for no): ")
    if day3.lower() == 'y':
        day3= True
    elif day3.lower() == 'n':
        day3= False
    else:
        print("Invalid entry. Defaulting to no.")
        day3=False

    habit.complete(day1)
    habit.complete(day2)
    habit.complete(day3)

    print("Progress status:", habit.evaluate_progress())


    