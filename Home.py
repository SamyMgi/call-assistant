# =============================================================================
# Main screen of the CallAssistant application.
# =============================================================================

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
import CallAssistant as ca
import User as us

class Home(GridLayout) :
    def __init__(self) :
        super(Home, self).__init__()
        
        #Predefined Assistant
        self.profile = ca.CallAssistant()
        
        #Predefined User
        self.user = us.User("John")
        self.user.predefinedPlanning()
        
        self.cols = 1
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.add_widget(Image(source='img/assistant.png'))
        self.call = Button(text="Simulate call", size_hint = (0.5, 0.2), bold = True)
        self.call.bind(on_press=self.callback)
        self.add_widget(self.call)
        self.instructions = Label(text="")
        self.add_widget(self.instructions)

    def simulate_call(self) :
        """
        Simulate the CallAssistant interaction.

        Returns
        -------
        None.

        """
        print("Let's call !")
        self.profile.call(self.user)
        self.instructions.text = str(self.profile.decision)
        
    def callback(self, instance):
        self.simulate_call()  
        
class CallAssistantApp(App) :
    def build(self) :
        return Home()
    
