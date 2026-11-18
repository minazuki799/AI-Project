WARNING_SIGN = "warning_sign"

# Keys --> meaning --------------------------------------------------------
# "memory_loss" --> Memory loss	
# "confusion_time_place" --> Confusion about time or place
# "familiar_tasks" --> Difficulty completing familiar tasks
# "language" --> Problems speaking or finding words
# "misplacing" --> Misplacing objects
# "judgement" --> Poor judgment or decision-making
# "mood_personality" --> Mood or personality changes
# "withdrawal" --> Withdrawal from social activities
# "planning" --> Difficulty planning or solving problems	
# "visual_spatial" --> Trouble understanding visual images or spatial relationships
	
# answer dictionary to hold answer to questions
answer = {
    "memory_loss" : "",
    "confusion_time_place" : "",
    "familiar_tasks" : "",
    "language" : "",
    "misplacing" : "",
    "judgment" : "",
    "mood_personality" : "",
    "withdrawal" : "",
    "planning" : "",
    "visual_spatial" : ""
}

questions = {
        "memory_loss":{ 
            "question": "Have you noticed new memory problems that happen often and disrupt daily life?",
            "examples" : ["Forgetting recently learned information","Repeatedly asking the same question","Forgetting important dates or events","Repeating statements"],
            "group": WARNING_SIGN},
        "confusion_time_place" : {
            "question": "Have you noticed new confusion about the time, the date or where you are that happens often and disrupts daily life??",
            "examples" : ["Getting lost in familiar places"],
            "group": WARNING_SIGN}, 
        "familiar_tasks" : {
            "question": "Have you noticed new difficulty completing familiar tasks that happens often and disrupts daily life?",
            "examples" : ["Inability to follow familiar procedures","Difficulty completing daily tasks"],
            "group": WARNING_SIGN},
        "language" : {
            "question": "Have you noticed new problems speaking or finding the right words that happen often and disrupt daily life?",
            "examples" : ["Difficulty following conversations"],
            "group": WARNING_SIGN},
        "misplacing" : {
            "question": "Have you noticed new problems misplacing things and being unable to retrace your steps that happen often and disrupt daily life?",
            "examples" : ["Putting things in unusual places", "Being unable to retrace steps to find an item."],
            "group": WARNING_SIGN},
        "judgment" : {
            "question": "Have you noticed new poor decisions or poor judgment that happen often and disrupt daily life?",
            "examples" : ["Unwise decisions with money", "Paying less attention to grooming"],
            "group": WARNING_SIGN},
        "mood_personality" : {
                    "question": "Have you noticed new changes in mood or personality that happen often and disrupt daily life?",
                    "examples" : ["Increased anxiety", "Personality changes"],
                    "group": WARNING_SIGN},
        "withdrawal" : {
                    "question": "Have you noticed new withdrawal from work, hobbies or social activities that happens often and disrupts daily life?",
                    "examples" : ["Dropping hobbies or social activities", "Avoiding family gatherings or work"],
                    "group": WARNING_SIGN},
        "planning" : {
                    "question": "Have you noticed new difficulty planning or solving problems that happens often and disrupts daily life?",
                    "examples" : ["Trouble following a familiar recipe", "Trouble keeping track of monthly bills"],
                    "group": WARNING_SIGN},
        "visual_spatial" : {
                    "question": "Have you noticed new trouble understanding what you see or judging distances that happens often and disrupts daily life?",
                    "examples" : ["Trouble understanding visual and spatial relationships","Difficulty reading", "Difficulty judging distance"],
                    "group": WARNING_SIGN},      
}  


class RuleAlzheimer:

    def __init__(self,answer:dict):
        self.answer = answer
        self.assumption = "Team assumption"
        self.confidence_disclaimer = (
            "Note: Confidence scores (0.0-1.0) reflect rule-matching strength and data completeness, NOT calibrated clinical probability."
        )
    def calculate_confidence(self,weighted_prob:float):
        '''
        confidence = weighted_probability * ((total_questions-unknown_questions)/total_questions)
        
        '''
        unknown_count = sum(1 for value in self.answer.values() if value == "don't know")
        data_completeness = (len(self.answer) - unknown_count)/len(self.answer)
        return round(weighted_prob * data_completeness,2)
    
    def print_rules(self):
        '''
            returns [(conclusion,confidence,advice,reason,source,str(rule))]
            
        '''
        self.rules = []
        no_of_signs = sum(1 for value in self.answer.values() if value == "yes")
            # compound rules
        if  no_of_signs == 2:
            self.rules.append(("Possible cognitive decline",self.calculate_confidence(0.60),"Schedule a routine healthcare evaluation","Two signs affecting more than one area of daily life",self.assumption,"If there are two signs or symptoms then possible cognitive decline, recommend a routine healthcare evaluation" ))
        elif 3 <= no_of_signs <= 4:
            self.rules.append(("Possible early Alzheimer's indicators",self.calculate_confidence(0.70),"Seek professional cognitive assessment","Three or four signs affecting multiple areas of daily life indicates a cluster",self.assumption,"If there are three or four signs or symptoms then possible early indicators, recommend a professional cognitive assessment" ))
        elif no_of_signs == 5:
            self.rules.append(("Moderate Alzheimer's warning signs",self.calculate_confidence(0.80),"Consult a healthcare professional for further evaluation","Five signs affecting multiple areas of daily life indicates a cluster",self.assumption,"If there are five signs or symptoms then moderate Alzheimer's warning signs, recommend consulting a healthcare professional for further evaluation" ))
        elif no_of_signs >= 6:
            self.rules.append(("Strong Alzheimer's warning signs",self.calculate_confidence(0.90),"Seek comprehensive medical and cognitive assessment","Six or more signs affecting multiple areas of daily life indicates a significant likelihood of Alzheimer's disease",self.assumption,"If there are six or more signs or symptoms then strong Alzheimer's warning signs, recommend seeking comprehensive medical and cognitive assessment" ))
             
        
        # base rules --> When only one sign is observed
        base_rules = {

            "memory_loss": (
                "Possible memory impairment",
                "Monitor memory changes and keep records.",
                "Memory problems may indicate changes in memory functioning."
            ),

            "confusion_time_place": (
                "Possible orientation concern",
                "Seek professional cognitive assessment.",
                "Confusion about time or place may indicate changes in orientation."
            ),

            "familiar_tasks": (
                "Possible difficulty with daily functioning",
                "Schedule a routine healthcare evaluation.",
                "Difficulty completing familiar tasks may indicate changes in daily functioning."
            ),

            "language": (
                "Possible communication concern",
                "Consult a healthcare professional.",
                "Difficulty finding words or following conversations may indicate communication changes."
            ),

            "misplacing": (
                "Possible memory-related concern",
                "Monitor memory changes and keep records.",
                "Frequently misplacing objects may indicate changes in memory functioning."
            ),

            "judgment": (
                "Possible judgment concern",
                "Arrange a healthcare evaluation.",
                "Poor judgment may indicate changes in decision-making abilities."
            ),

            "mood_personality": (
                "Possible behavioural changes",
                "Consult a healthcare professional.",
                "Changes in mood or personality may indicate behavioural changes."
            ),

            "withdrawal": (
                "Possible social withdrawal concern",
                "Monitor changes in social participation.",
                "Withdrawal from social activities may indicate changes in everyday functioning."
            ),

            "planning": (
                "Possible planning and reasoning concern",
                "Schedule a healthcare evaluation.",
                "Difficulty planning or solving problems may indicate changes in reasoning."
            ),

            "visual_spatial": (
                "Possible visual-spatial concern",
                "Seek professional assessment.",
                "Difficulty understanding visual information may indicate visual-spatial changes."
            )
        }

        if no_of_signs == 1:

            for sign, details in base_rules.items():

                if self.answer[sign] == "yes":

                    conclusion, advice, reason = details

                    self.rules.append((
                        conclusion,
                        self.calculate_confidence(0.40),
                        advice,
                        reason,
                        self.assumption,
                        f"IF {sign} = yes THEN {conclusion}"
                    ))

                    break

        if no_of_signs == 0:

            unknown_count = sum(
                1 for value in self.answer.values()
                if value == "don't know"
            )

            if unknown_count > 0:

                self.rules.append((
                    "Insufficient information",
                    self.calculate_confidence(0.0),
                    "Collect additional information before reaching a conclusion.",
                    "No warning signs were confirmed, but some responses were unknown.",
                    self.assumption,
                    "IF no warning signs are confirmed AND some answers are unknown THEN insufficient information"
                ))

            else:

                self.rules.append((
                    "No warning signs reported",
                    self.calculate_confidence(0.0),
                    "No warning signs were reported. Seek professional advice if concerns arise.",
                    "None of the ten warning signs were reported.",
                    self.assumption,
                    "IF all warning signs = no THEN no warning signs reported"
                ))

        return self.rules

'''
certainty weights
	• 0 sign: 0.00 
	• 1 sign: 0.40 
	• 2 signs: 0.60 
	• 3-4 signs: 0.70 
	• 5 signs: 0.80 
	• 6+ signs: 0.90 
 (CDC notes 1 disruptive sign warrants a doctor visit)
'''

# i was trying to play around with the code to test it out to know if it would work sha commented it out, i no know sha boss
# # if __name__ == "__main__":

#     answers = {
#         "memory_loss": "yes",
#         "confusion_time_place": "no",
#         "familiar_tasks": "no",
#         "language": "no",
#         "misplacing": "no",
#         "judgment": "no",
#         "mood_personality": "no",
#         "withdrawal": "no",
#         "planning": "no",
#         "visual_spatial": "no"
#     }

#     system = RuleAlzheimer(answers)

#     results = system.print_rules()

#     for result in results:
#         print(result)


