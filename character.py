import random

def get_character() -> str:
    #hair color, hair length, eye color
    colors = ["Red", "Orange", "Blue", "Yellow", "Green", "Pink", "Purple", "Brown", "Grey", "White", "Black"]
    lengths = ["Short", "Mid-Length", "Long"]
    size = ["Thin", "Twunk", "Bigggg!"]
    moneys = ["Broke", "Lower Average", "Average", "Rich", "Too Rich"]
    addictions = ["No", "Moderately", "Addict"]
    health = ["Alive", "Dead :(", "Alive but lowkey dying..."]

    hairColor = random.choice(colors)
    hairLen = random.choice(lengths)
    eyeColor = random.choice(colors)
    bodySize = random.choice(size)
    familyHealth = random.choice(health)

    familyFinance = random.choice(moneys)
    personalFinance = random.choice(moneys)

    alcohol = random.choice(addictions)
    cigarette = random.choice(addictions)
    gambling = random.choice(addictions)

    # mid height = 170
    height = random.randint(150, 200)

    mole = random.choice((True,False))
    moleNum = 0
    if mole:
        moleNum = random.randint(1,5)
    
    character = f"""## Character Generator
        > **Hair** : {hairLen} {hairColor} 
        > **Eye Color** : {eyeColor} 
        > **Height** : {height} CM
        > **Body Size** : {bodySize} 
        > **Moles** : {moleNum} 
        > 
        > **Family** : {familyHealth}  
        > **Born Into(Family Wealth)** : {familyFinance} 
        > **Personal Wealth** : {personalFinance} 
        > 
        > **Drinking** : {alcohol} 
        > **Smoking** : {cigarette} 
        > **Gambling** : {gambling} 
        """
    return character