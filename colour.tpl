% rebase('base.tpl', title="Farge")

<!-- {{'''Liste med RGB-verdier'''}} -->
% import random
% colourList = ["red", "blue", "green"]
% randColour = random.choice(colourList)

<body style="background-color: {{randColour}}; id=Bakgrunn";>

