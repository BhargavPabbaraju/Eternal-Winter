

TOWNNAME="Barafia"

texts={
'intro':["%s...\n"%TOWNNAME + "Once a beautiful island full of greenery\n" + "Has been cursed with eternal winter for nearly twenty years\n"+\
            "Prophecies say a hero shall be born to end the curse"],


'sci':[

#0 Intro text when first met
"You've managed to come this far? You must be the hero the prophecies predicted.\n"+"My name is Frost, I am a scientist.\n"+\
"I invented a device that could manipulate the weather.\n"+"The device malfunctioned and brought an eternal winter to %s.\n"%TOWNNAME +\
"The device's core parts scattered into pieces all over %s.\n"%TOWNNAME + "If we gather all the pieces maybe I can reset the weather.\n",

#1 If all gems are not collected
"Hmm...You haven't gathered all the pieces yet\n",

#2 If all gems are collected
"Looks like you collected all the pieces!\n"+"There is one more essential ingridient into resetting the weather.\n"+"I can't seem to remember what that might be\n"+\
"Oh well it is surely somewhere in %s\n."%TOWNNAME,

#3 If speical ingrident not found
"Oh well it is surely somewhere in %s\n."%TOWNNAME,

#4 If speical ingrident found
"That's it! I craved some hot coffee for many years.\n"+"You truly are a hero just as the prophecies say.\n",

#5 Resetting the weather
"This here....that there.... and....\n"+"......\n"+"All done! This should work.\n",

#6 After reset
"Eureka! The greenery is back.\n"+"No more sneezing and coughing.\n" +"You truly are a hero. You saved %s"%TOWNNAME

]
}
