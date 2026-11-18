class InferenceEngine:
    def __init__(self,questions:dict,answers:dict,rule_class):
        self.questions = questions
        self.answers = answers
        self.rule_class = rule_class
    
    def ask_questions(self):
        for symptom,dictionary in self.questions.items():
            x = True # break element
            while x:
                ans = input(f"{dictionary["question"]}\n").strip().lower()
                if ans in ["yes","no","don't know"]:
                    x = False # break element
                    self.answers[symptom] = ans
                elif ans == 'example':
                    print(dictionary["examples"])
                else:
                    print("Answer must be either 'yes','no' or 'don't know'. Type 'example' to see some sample cases")
    
    def forward_chaining(self):
        pass
    
    def backward_chaining(self):
        pass
    
    def explain(self):
        pass