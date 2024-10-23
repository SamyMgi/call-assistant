# =============================================================================
# Class to create a Call Assistant who asks questions to the caller, get the answers, 
# and ask Gorgias Cloud API to get decision.
# =============================================================================

import logging
import time
import datetime
import requests
import login

import speech_recognition as sr
import pyttsx3 as tts

class CallAssistant :
    def __init__(self) :      
        #Predefined tree and questions
        self.tree = {"Bonjour, qui êtes vous ?" : ["AMI", "FAMILLE", "AUTRE"], "Est-ce ?" : ["URGENT", "PAS URGENT"]}
        self.lex = {"START" : "Bonjour, qui êtes vous ?", "FAMILLE" : "Est-ce ?"}
        #To convert into prolog notation
        self.lex_to_pl = {"AMI" : "friend(Call)", "FAMILLE" : "family(Call)", "URGENT" : "emergency", "REPAS" : "at_lunch", "REUNION":"at_meeting", "TRAVAIL" : "at_work"}
        #Answers in prolog
        self.answers_to_send = []
        #All user's answers
        self.answers_tmp = []
        #User's final answers
        self.answers = []
        #API's decision
        self.decision = False


    
    def __convert_speech_to_text(self, recognizer, audio):
        """
        Callback to get microphone answers
        """
        try:
            answer = recognizer.recognize_google(audio, language = "fr-FR")
            self.answers_tmp.append(answer.upper())
            print(answer)
        except sr.UnknownValueError:
            logging.warning("Failed to understand audio")
            self.answers_tmp.append(None)
        except sr.RequestError:
            logging.warning("Couldn't request Gooogle Speech Recognition Service")
            self.answers_tmp.append(None)

    def questioning(self, noisy = False) :
        """
        Ask questions to the caller and get his answers.

        Parameters
        ----------
        noisy : BOOLEAN, optional
            If True, adapt to noisy places. The default is False.

        Returns
        -------
        None.

        """
        self.answers_tmp = [""]     
        self.answers = []
        WORD = "START"
        
        #Initialize Text-To-Speech engine
        engine = tts.init()
        
        #Ask each questions
        while WORD in self.lex.keys() :    
            engine.say(self.lex[WORD])
            engine.runAndWait()
    
            for possible_answer in self.tree[self.lex[WORD]] :
                engine.say(possible_answer)
                engine.runAndWait()
            
            repetition = False
            
            while self.answers_tmp[-1] not in self.tree[self.lex[WORD]] :
                if repetition == True : 
                    engine.say("Veuillez recommencer") 
                    engine.runAndWait()
                
                repetition = True
                
                #Initialize Speech-To-Text engine
                r = sr.Recognizer()
                m = sr.Microphone()
                
                if noisy :
                    with m as source:
                        r.adjust_for_ambient_noise(source, duration = 2)
                        
                stop_listening = r.listen_in_background(m, callback = self.__convert_speech_to_text)
                logging.info("Hearing...")
                time.sleep(6)
                logging.info("Waiting...")
                stop_listening(wait_for_stop=False)
                time.sleep(2)
                
            self.answers.append(self.answers_tmp[-1])
            logging.info("End")
            WORD = self.answers[-1]
    

    def refine_answers(self, user) :
        """
        Allows to refine decision by adding user's planning status. 

        Parameters
        ----------
        user : USER
            User's profile.

        Returns
        -------
        None.

        """
        
        now = datetime.datetime.now().hour
        if user.planning[now] != "" :
            self.answers.append(user.planning[now].upper())
        logging.info(str("Answers :" + '-'.join(self.answers)))


    def __answers_to_json(self, caller_name="john", gorgias_file = login.file) :
        """
        Convert user's answers in prolog premises and convert them to JSON.

        Parameters
        ----------
        caller_name : STRING, optional
            Caller's name. The default is "john".
        gorgias_file : STRING, optional
            Path to the pl file. The default is the "file" from login.py.

        Returns
        -------
        answers_json : JSON
            Answers to send to the API.

        """
        self.answers_to_send = []
        for answer in self.answers :
            if answer in self.lex_to_pl.keys() :
                self.answers_to_send.append(self.lex_to_pl[answer].replace("Call", caller_name))
        
        answers_json = {"facts": [str("phone_call("+caller_name+")")],"gorgiasFiles": [gorgias_file],"query": str("allow("+caller_name+")"),"resultSize": 1}
        
        for answer in self.answers_to_send :
            answers_json["facts"].append(answer)
            
        return answers_json
    
    def get_decision(self) :
        """
        Send answers to the Gorgias API to get the decision.

        Returns
        -------
        None.

        """
        request = requests.post("http://aiasvm1.amcl.tuc.gr:8085/GorgiasQuery", auth=(login.user, login.passwd), json=self.__answers_to_json())
        decision_str = request.text[13:17]
        if decision_str == "true" :
            self.decision = True
        else :
            self.decision = False
        logging.info(str("Final decision :"+str(self.decision)))
        
    
    def postpone(self, user) :
        """
        Finds the best time at which the caller should call back by 
        testing the status of the next hours of the day.
        ----------
        user : USER
            User's profile.

        Returns
        -------
        None.

        """
        now = datetime.datetime.now().hour
        status = user.planning[now]
        status_pos = self.answers.index(status)
        engine = tts.init()
        already_seen = [status]
        
        for slot in range(now+1,24) :
            next_status = user.planning[slot]
            if next_status not in already_seen:
                already_seen.append(next_status)
                self.answers[status_pos]=next_status
                self.get_decision()
                logging.info(str("Answers :" + '-'.join(self.answers_to_send)))
                if self.decision == True :
                    to_say = "Veuillez rappeler vers"+str(slot)+"heures"
                    engine.say(to_say)
                    engine.runAndWait()
                    break
        if self.decision == False :
            to_say = "Il n'est pas disponible pour le moment."
            engine.say(to_say)
            engine.runAndWait()
        
        to_say = "Au revoir"
        engine.say(to_say)
        engine.runAndWait()
            
        
    def endphase(self, user) :
        """
        End of the call. 
        Two possibilities : 
            *Refuse the call by proposing to call later at a specific hour.
            *Allow the call and link the caller to the user.

        Parameters
        ----------
        user : USER
            User's profile.

        Returns
        -------
        None.

        """
        if self.decision == False :
            self.postpone(user)
        else :
            engine = tts.init()
            to_say = "Vous allez être mis en relation avec votre interlocuteur."
            engine.say(to_say)
            engine.runAndWait()
 
    def call(self, user) : 
        """
        Manage user's call.

        Parameters
        ----------
        user : USER
            User's profile.

        Returns
        -------
        None.

        """
        self.questioning()
        self.refine_answers(user)
        self.get_decision()
        self.endphase(user)
            
