# importing modules --> Inference Engine and knowledge bases
import sys
from colorama import Fore, init
import textwrap
from inferenceengine import InferenceEngine 


message = Fore.GREEN + "Successfully Imported All Knowledge Bases and Inference Engine" + Fore.RESET
print(message)
disclaimer = "This is a rule-based expert that uses knowledge representation and logical reasoning to provide preliminary decision support for narrowly defined health related scenarios. This knowledge bases in this system only represents Alzheimer's disease and diabetes. This remains an educational tool  It is not a tool for real-world diagnosis. "
print(textwrap.fill(disclaimer, width=50))

# User Input Helper Function
def ask(message,warning,constraint:list):
    while True:
        try:
            choice = int(input(message))
            if choice not in constraint:
                print(warning)
            else:
                return choice
        except ValueError:
            print(warning)

# Selecting knowledge base
warning = Fore.YELLOW + "Warning: you must select integers (1,2)" + Fore.RESET
load_message =("Select scenario:\nEnter 1 ---> Alzheimer's disease.\nEnter 2 ---> Diabetes\n")
constraint = [1,2]
choice = ask(load_message,warning,constraint)

# loading knowledge base
if choice == 1:
    from alzheimer import goals,questions,answer,contradictions,RuleAlzheimer # Alzheimer's KB
    system = InferenceEngine(
    questions= questions,
    answers = answer.copy(), # so original answer in KB is not overwritten
    rule_class = RuleAlzheimer,
    contradictions=contradictions,
    goals=goals    
    )
else:
    pass # no diabetes KB to pull from

# Selecting method (forward_chaining or backward_chaining)
method_warning = Fore.YELLOW + "Warning: you must select integers (1,2)" + Fore.RESET
method_message =("Select method:\nEnter 1 ---> Forward chaining.\nEnter 2 ---> Backward chaining\n")
method_constraint = [1,2]
method_choice = ask(method_message,method_warning,method_constraint)

if method_choice == 1:
    system.forward_chaining()
elif method_choice == 2:
    system.backward_chaining()

# Explain or exit system 
explain_warning = Fore.YELLOW + "Warning: you must select integers (1,2)" + Fore.RESET
explain_message =("Enter 1 ---> Explain results.\nEnter 2 ---> Quit\n")
explain_constraint = [1,2]
explain_choice = ask(explain_message,explain_warning,explain_constraint)

if explain_choice == 1:
    system.explain_rules()
    sys.exit(Fore.CYAN + "Session Ended" + Fore.RESET)
else:
    sys.exit(Fore.CYAN + "Session Ended" + Fore.RESET)

    


