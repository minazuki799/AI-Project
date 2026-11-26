# imports
import pprint
from tabulate import tabulate
from colorama import Fore, init
init(autoreset=True,strip=False)

class InferenceEngine:
    def __init__(self,questions:dict,answers:dict,rule_class,contradictions:list,goals:dict,symptoms_dictionary:dict):
        self.questions = questions
        self.answers = answers
        self.symptoms_dictionary = symptoms_dictionary
        self.kb = rule_class(self.answers)
        self.contradictions = contradictions
        self.unresolved_contradictions = [] 
        self.goals = goals # for backtracking
        self.follow_up_asked = set()
        self.input_error_message = "Answer must be either 'yes','no' or 'don't know'. Type 'example' to see some sample cases"
    
    def ask_questions(self):
        for symptom,dictionary in self.questions.items():
            x = True # break element
            while x:
                ans = input(f"{dictionary['question']}\n").strip().lower()
                if ans in ["yes","no","don't know"]:
                    x = False # break element
                    self.answers[symptom] = ans
                elif ans == 'example':
                    print(dictionary['examples'])
                else:
                    print(Fore.RED + self.input_error_message)
    
    def check_inconsistencies(self):
        self.unresolved_contradictions.clear()
        for symptom1,symptom2 in self.contradictions:
            if {self.answers[symptom1],self.answers[symptom2]} == {"yes","no"}:
                print(Fore.YELLOW + "Warning: Inconsistency found!\nPossible Inconsistence detected between symptoms ",self.symptoms_dictionary[symptom1]," and ",self.symptoms_dictionary[symptom2])
                #clarification
                choice = input("\nWould you like to review and update these answers? (yes/no)").strip().lower()
                if choice == 'yes':
                    for symptom in [symptom1,symptom2]:
                        x = True
                        while x:
                            ans = input(f"{self.questions[symptom]['question']}\n").strip().lower()
                            if ans in ["yes","no","don't know"]:
                                x = False # break
                                self.answers[symptom] = ans
                            elif ans == 'example':
                                print(self.questions[symptom]['examples'])
                            else:
                                print(Fore.RED + self.input_error_message)
                
                # record if contradictory
                if {self.answers[symptom1],self.answers[symptom2]} == {"yes","no"}:
                    self.unresolved_contradictions.append((self.symptoms_dictionary[symptom1],self.symptoms_dictionary[symptom2]))
    
    def ask_follow_up_questions(self): 
        for symptom, answer in self.answers.items():

            if answer == "don't know" and symptom not in self.follow_up_asked:

                self.follow_up_asked.add(symptom)

                print(Fore.YELLOW + "\nFollow-up question for " + symptom.replace("_", " ").title())

                while True:
                    response = input(
                        self.questions[symptom]["follow_up_question"] + "\n"
                    ).strip().lower()

                    if response == "yes":

                        # Update the original answer dictionary
                
                        self.answers[symptom] = "yes"

                        print(Fore.GREEN + "Answer updated to yes.")
                        break

                    elif response in ["no", "don't know"]:

                        # Leave the original answer as don't know
                        print("No change made. Answer remains don't know.")
                        break

                    else:
                        print(Fore.RED + self.input_error_message)
    
    def present_conclusions(self,results:list):
        '''
        results = [(conclusion,confidence,advice,reason,source,str(rule))]
        '''
        print("Rule-Based Expert System for Medical Decision Support.\nAll rules are illustrative and are not intended for actual diagnosis")
        rows = []
        for result in results:
            conclusion,confidence,recommendation,rationale,source,rule = result
            rows.append([
                Fore.GREEN + conclusion + Fore.RESET,
                confidence,
                Fore.CYAN + recommendation + Fore.RESET,
                rationale,
                source,
                rule
                ])
        
        # printing--------------------------------------------------------------------------   
        print(tabulate(rows,headers=["Conclusion","Confidence_score","Recommendation","Rationale","Source","Rule as text"], tablefmt="grid", maxcolwidths=[22, 10, 24, 28, 16, 32]))
        
        # printing unresolved contradictions if present
        if self.unresolved_contradictions:
            print(Fore.YELLOW + f"\nWarning - Contradictory Evidence Noted." + Fore.RESET)
            pprint.pprint(self.unresolved_contradictions, indent=2)
        
        if hasattr(self.kb, "confidence_disclaimer"):
            print(f"\n{self.kb.confidence_disclaimer}")
                    
    def forward_chaining(self):
        if not all(answer != "" for answer in self.answers.values()): # check if all questions has been answered
            self.ask_questions()  
            
        self.check_inconsistencies() # check inconsistencies with answers
        self.ask_follow_up_questions() # follow up questions 
        
        # forward chaining
        triggered_rules = self.kb.print_rules() # expects [(conclusion,confidence,advice,reason,source,str(rule))]
        
        self.present_conclusions(triggered_rules) 

    def ask_question_backtrack(self,condition:int):
        yes_count = 0
        no_count = 0
        for symptom,dictionary in self.questions.items():
            x = True # break element
            while x:
                ans = input(f"{dictionary['question']}\n").strip().lower()
                if ans in ["yes","no","don't know"]:
                    self.answers[symptom] = ans
                    if ans == "yes":
                        yes_count += 1
                        if yes_count == condition: # set all unawsered questions to "don't know"
                            for key,value in self.answers.items():
                                if value == "":
                                    self.answers[key] = "don't know"
                            return (True,yes_count,no_count) # stopping early if condition is met
                
                    else: # ans is not "yes"
                        no_count += 1
                        if no_count == (len(self.questions) - condition) + 1: # impossible to meet condition
                            for key, value in self.answers.items():
                                if value == "":
                                    self.answers[key] = "don't know" # useful so we can audit rules after a failed backtracking
                            return (False,yes_count,no_count) # stopping early due to imposibility
                    x = False # break
                elif ans == 'example':
                    print(dictionary['examples'])
                else:
                    print(Fore.RED + self.input_error_message)
                    
        return (False, yes_count, no_count)
                            
    def backward_chaining(self):
        print(Fore.WHITE + "Initializing backward_chaining...\n" + Fore.RESET,"Please select a hypothesis from the options below:\n")
        goal_index_list = list(self.goals.keys())
        i = 1
        for goal in self.goals.keys(): # might cause error
            print(f"Enter {i} to select {goal}")
            i += 1
        while True:
            try:
                choice = int(input("Choice: "))
                if 1 <= choice <= len(self.goals):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.goals)}.")
            except ValueError:
                print("Only enter the numbers prompted")
        condition = self.goals[goal_index_list[choice-1]] # condition for hypothesis (int)
        # asks questions ---------------------------
        for key in self.answers: # reset anwsers so backward_chaining begins with fresh dictionary
            self.answers[key] = ""

        status,yes_count,no_count = self.ask_question_backtrack(condition) 
        # printing results of backward_chaining------------------
        if status:
            print(Fore.GREEN + f"Sucess, all {condition} conditions for {goal_index_list[choice-1]} hypothesis met!\n" + Fore.RESET,"")
            # printing results
            triggered_rules = self.kb.print_rules() # expects [(conclusion,confidence,advice,reason,source,str(rule))]
            self.present_conclusions(triggered_rules)  
           
        else:
            print(Fore.RED + f"Failure, Could not meet the {condition} conditions for {goal_index_list[choice-1]} hypothesis, only {yes_count} were met before stopping!\n" + Fore.RESET,"")
    
    def explain_rules(self):
        '''
        Explains why each rule was accepted or rejected using self.kb.audit_rules()
        '''
        
        if hasattr(self.kb, "audit_rules"):
            rows = []
            result = self.kb.audit_rules() #(rule_id,conclusion,status,reason)
            for rule_id,conclusion,status,reason in result:
                if status == "Fires":
                    status = Fore.GREEN + status + Fore.RESET
                elif status == "Cannot be evaluated":
                    status = Fore.YELLOW + status + Fore.RESET
                else:
                    status = Fore.RED + status + Fore.RESET
                rows.append([
                    rule_id,
                    conclusion,
                    status,
                    reason
                    ])
            
            # printing--------------------------------------------------------------------------   
            print(tabulate(rows,headers=["Rule_id","Conclusion","Status","Reason"], tablefmt="grid", maxcolwidths=[15, 28, 10, 28]))
    
            
         
            
        
        
        
        
    