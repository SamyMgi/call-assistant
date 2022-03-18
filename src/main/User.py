class User :
    def __init__(self, name) :
        self.name = name
        self.planning = ["" for i in range(24)]
        
    
    def addInPlanning(self, start, end, state) :
        for i in range(start, end) :
            self.planning[i] = state
    
    def getPlanning(self) :
        for i in range(0, len(self.planning)) :
            print(i, " - ", i+1, " : ", self.planning[i])
        
    def predefinedPlanning(self) :
        self.addInPlanning(10,12,"Réunion")
        self.addInPlanning(12,13,"Repas")
        self.addInPlanning(0,6,"Indisponible")
        self.addInPlanning(17,18,"Réunion")
        self.addInPlanning(21,24, "Indisponible")