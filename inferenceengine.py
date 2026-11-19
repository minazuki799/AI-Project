# imports
import pprint
from tabulate import tabulate
from colorama import Fore, init
init(autoreset=True,strip=False)

class InferenceEngine:
    def __init__(self,questions:dict,answers:dict,rule_class,contradictions:list):
        self.questions = questions
        self.answers = answers
        self.kb = rule_class(self.answers)
        self.contradictions = contradictions
        self.unresolved_contradictions = []
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
                print(Fore.YELLOW + "Warning: Inconsistency found!\nPossible Inconsistence detected between ",symptom1," and ",symptom2)
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
                    self.unresolved_contradictions.append((symptom1,symptom2))
    
    def ask_follow_up_questions(self):
        follow_up_questions = {
            "memory_loss": "Have you recently forgotten important information, such as appointments or conversations?",
            
            "confusion_time_place": "Have you recently become confused about where you are or what day or date it is?",
            
            "familiar_tasks": "Have you recently struggled to complete everyday activities you previously knew how to do?",
            
            "language": "Have you recently struggled to find the right words or follow conversations?",
            
            "misplacing": "Have you recently misplaced everyday items and struggled to remember where you put them?",
            
            "judgment": "Have you recently made unusual decisions or decisions that are out of character for you?",
            
            "mood_personality": "Have people close to you noticed unusual changes in your mood or personality?",
            
            "withdrawal": "Have you recently lost interest in hobbies, work or spending time with other people?",
            
            "planning": "Have you recently struggled to organise tasks or solve familiar problems?",
            
            "visual_spatial": "Have you recently had difficulty judging distances or understanding visual information?"
        }
        
        for symptom, answer in self.answers.items():

            if answer == "don't know" and symptom not in self.follow_up_asked:

                self.follow_up_asked.add(symptom)

                print(Fore.YELLOW + "\nFollow-up question for " + symptom.replace("_", " ").title())

                while True:
                 response = input(
                    follow_up_questions[symptom] + "\n"
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

    
    def backward_chaining(self):
        pass
    