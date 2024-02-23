import random

def get_response(userInput) -> str:
    lowered: str = userInput.lower()
    num = random.randint(1, 10)

    if lowered == '':
        return ':3 ' * num
    elif any(x in lowered for x in ['hello', 'hey', 'hewwo']):
        return 'hey' * num + '!!'
    elif 'bye' in lowered:
        return 'nya!'
    elif 'love' in lowered:
        return "......:3"
    elif any(x in lowered for x in ['snek', 'snake', 'ssss']):
        return "noodle noodle nyanya~"
    elif 'you' in lowered:
        return 'More importantly how are you? Are your crops water? Are your works done? Is that art wip finish??'
    else:
        res = [
            "damn...",
            userInput + " :3?" ,
            "Murder is okay!!", 
            "Yes",
            "No :3c", 
            ":thinking:", 
            "Idk what you saying but you doing great!",
            "You ok buddy?"
            ]
        
        num = random.randint(0, len(res)-1)
        return res[num]