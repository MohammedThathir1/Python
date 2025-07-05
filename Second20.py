import logging
import multiprocessing
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for the conversation
QUESTION_STATES = list(range(8))  # Adjust the range if the number of questions varies per bot

# Example questions for 30 different bots 
questions_list = [
    # Questions for Bot 1
    [   # Questions for Bot 11
        {"question": '''A, B and C can do a piece of work in 20, 30 and 60 days respectively. In how many days can A do the work if he is assisted by B and C on every third day?''', "answer": 15},

        {"question": '''In a room where structures rise and fall,
And forces of nature answer the engineer's call.
Not a site where buildings are set in stone,
But a place where materials are tested alone.
Bridges, beams, and foundations take shape,
As calculations determine what can break.
Seek the lab where the strength of the earth is known,
And your clue lies where stability is shown. ''', "answer": 110},

        {"question": '''A car of mass 2000 kg is moving with a constant acceleration of 2 m/s2. Calculate the net force acting on the car''', "answer": 4000},

        {"question": '''In a chamber where invisible forces reign,
And the dance of fluids you must explain.
Not a sea nor a waterfall grand,
But a place where pressure meets a calculated hand.
Equations of flow and resistance are key,
As turbulent streams test what will be.
Seek the lab where water obeys no calm,
And your clue is hidden where chaos meets the balm ''', "answer": 67},

        {"question": '''Three resistors, R1=90 Ω, R2=45 Ω, and R3=15 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 10},

        {"question": '''In a hidden vault where silence hums,
And the heartbeat of data softly drums.
Not a space where hands craft or create,
But a room where networks and connections dictate.
Wires and lights blink in a coded stream,
Holding the power behind every machine’s dream.
Seek the place where information flows,
And your clue lies where the digital wind blows.   ''', "answer": 114},

        {"question": ''' What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a square where tension hangs by a thread,
And battles are fought with a flick of the head.
Not a field nor a ground where feet dig deep,
But a court where swift shadows leap and sweep.
A feathered projectile rules the air,
With every strike, precision and flair.
Find the space where victory’s chase is short,
And your clue lies where speed meets the court   ''', "answer": 4000},
    ],
    [   # Questions for Bot 12
        {"question": ''' A alone can do a piece of work in 6 days and B alone in 8 days. A and B undertook to do it for Rs. 3200. With the help of C, they completed the work in 3 days. How much is to be paid to C?''', "answer": 400},

        {"question": '''A Lab where you play with letter      ''', "answer": 217},

        {"question": ''' A car of mass 1000 kg is moving with a constant acceleration of 2 m/s2. Calculate the net force acting on the car''', "answer": 2000},

        {"question": '''In a place where reality slips from sight,
And digital worlds emerge from light.
Not bound by the rules of the world you see,
But crafted in code, both wild and free.
Illusions and truth are side by side,
In a lab where the real and virtual collide.
Seek the space where the unreal becomes clear,
And your clue lies where vision transcends the sphere       ''', "answer": 119},

        {"question": '''Three resistors, R1=90 Ω, R2=45 Ω, and R3=15 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 18},

        {"question": '''In a quiet room where futures are cast,
And the efforts of many are revealed at last.
Not a lecture hall where knowledge is taught,
But a space where your hard work is brought.
Numbers and letters seal your fate,
Marking your progress, whether early or late.
Seek the place where verdicts are shared,
And your clue lies where every score is declared    ''', "answer": 1},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a sanctum where silence guards the lore,
And countless stories wait behind each door.
Not a space where voices echo loud,
But a haven where knowledge is shrouded and proud.
Rows upon rows of wisdom in bound attire,
Shelved with care, where seekers inquire.
Find the realm where the past and present fuse,
And your clue hides where the written words are used      ''', "answer": 1100},
    ],
    [   # Questions for Bot 13
        {"question": '''A hall is 15 m long and 12 m broad. If the sum of the areas of the floor and the ceiling is equal to the sum of the areas of four walls, the volume of the hall is:''', "answer": 1200},

        {"question": '''In a workshop where precision carves its mark,
And machines hum with a calculated spark.
Not a forge where metals are simply shaped,
But a lab where exactness is finely draped.
Automated tools and codes guide the way,
Turning raw materials with intricate play.
Seek the space where cutting-edge designs are planned,
And your clue lies where craftsmanship is grand.     ''', "answer": 68},

        {"question": '''  A car of mass 500 kg is moving with a constant acceleration of 2 m/s2. Calculate the net force acting on the car''', "answer": 1000},

        {"question": '''In a chamber where arguments twist and weave,
And legal minds present their case to achieve.
Not a courtroom with judges in their seats,
But a stage where simulated justice meets.
Precedents and pleas are debated with flair,
In a realm where the future of law is laid bare.
Find the place where legal drama unfolds,
And your clue lies where every argument holds.   ''', "answer": 204},

        {"question": '''.) Three resistors, R1=150 Ω, R2=75 Ω, and R3=50 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 25},

        {"question": '''In a domain where circuits and currents align,
And the hum of power is measured in kind.
Not a room where simple wiring is done,
But a workshop where electrical visions are spun.
With tools that test and components that spark,
Precision is key in this electrically charged park.
Seek the space where theory meets hands-on play,
And your clue lies where wires and knowledge convey ''', "answer": 65},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''From this grand hall where knowledge takes flight,
The adventure begins, setting your path alight.
Where speakers engage and ideas are born,
Your journey starts here, with the dawn of the morn.
Seek where discussions and lectures unfold,
And your clue lies where the quest's story is told  ''', "answer": 1200},
    ],
    [   # Questions for Bot 14
        {"question": '''50 men took a dip in a water tank 40 m long and 20 m broad on a religious day. If the average displacement of water by a man is 4 m3, then the rise in the water level in the tank will be''', "answer": 25},

        {"question": '''In a domain where voltage and currents intertwine,
And circuits are designed with precision in line.
Not a space where basic components just play,
But a lab where power management holds sway.
With converters and controllers working in sync,
Find the lab where high-power systems are linked.
Seek the place where energy flows with control,
And your clue lies where electronics fulfill their role  ''', "answer": 28},

        {"question": ''' A car of mass 750 kg is moving with a constant acceleration of 2 m/s2. Calculate the net force acting on the car''', "answer": 1500},

        {"question": '''In a space where legal battles are simulated with grace,
And every argument tests the rules of the case.
Not a courtroom where real judgments are made,
But a stage where future lawyers' skills are displayed.
Precedents are cited, and arguments are keen,
In a setting where legal minds are seen.
Find the chamber where mock trials are fought,
And your clue lies where justice is sought.     ''', "answer": 204},

        {"question": ''' Three resistors, R1=60 Ω, R2=60 Ω, and R3=30 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 15},

        {"question": '''In a vault where digital whispers softly hum,
And the pulse of the network continuously strums.
Not a place where physical forms are made,
But where data and signals serenely cascade.
Wires and lights blink in a precise dance,
Holding the secrets of tech in their expanse.
Seek the room where servers silently reign,
And your clue lies where information is sustained. ''', "answer": 114},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a domain where metal and code combine,
And machines learn to move in a designed line.
Not a workshop where tools merely fit,
But a space where robots are programmed to emit.
Sensors and actuators create complex schemes,
Bringing automation to life through intricate dreams.
Find the lab where robotics come to play,
And your clue lies where mechanisms sway   ''', "answer": 68},
    ],
    [   # Questions for Bot 15
        {"question": '''A cistern 6m long and 4 m wide contains water up to a depth of 1 m 25 cm. The total area of the wet surface is''', "answer": 49},

        {"question": '''In a realm where algorithms weave and code unfolds,
And machines learn from data as the story is told.
Not a classroom where basic theories are discussed,
But a lab where artificial intelligence is robust.
Models are trained, and patterns emerge,
In a space where data and decisions converge.
Seek the place where virtual minds are designed,
And your clue lies where machine learning is refined    ''', "answer": 120},

        {"question": ''' A car of mass 250 kg is moving with a constant acceleration of 2 m/s2. Calculate the net force acting on the car''', "answer": 500},

        {"question": '''In a sanctuary where melodies take flight,
And rhythms and harmonies bring pure delight.
Not a stage where public performances shine,
But a room where music’s essence is refined.
Instruments rest, and notes fill the air,
Crafting tunes with skill and care.
Seek the space where sound and harmony blend,
And your clue lies where musical dreams transcend  ''', "answer": 29},

        {"question": ''' Three resistors, R1=150 Ω, R2=75 Ω, and R3=50 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 25},

        {"question": '''In a domain where devices seamlessly link,
And the web of connections makes systems think.
Not a place where simple circuits are made,
But where smart networks and sensors cascade.
From data streams to networks, everything is tied,
And the Internet of Things comes alive inside.
Find the lab where connectivity and intelligence blend,
And your clue lies where digital interactions transcend.''', "answer": 69},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a quiet nook where devotion takes its place,
And the goddess of knowledge offers her grace.
Not a hall where wisdom is loudly proclaimed,
But a hidden sanctuary where reverence is named.
Behind where the reception’s welcome is near,
Find the symbol of learning held dear.
Seek where divine wisdom silently stands,
And your clue lies where sacred knowledge expands  ''', "answer": 3000},
    ],
     # Questions for Bot 1
    [
        {"question": " If two current phasors, having magnitude 12A and 5A intersect at an angle of 90 degrees, calculate the resultant current.", "answer": 13},
        
        {"question": '''In this space, I bend and break,
The laws of nature for knowledge’s sake.
Waves, forces, and energy collide,
Where theories of motion never hide.
I make the apple fall, the pendulum swing,
In my domain, even light takes wing.
If you're searching for truth in the unknown,
Find where experiments are carefully shown.''', "answer": 13},
        
        {"question": " How many types of cement are there based on the ability to set in presence of water?", "answer": 2},
        
        {"question": '''I speak in tongues, yet make no sound,
Where voices and accents can be found.
I help you master words you seek,
To speak in ways unique and sleek.
Where listening is key and mimicry reigns,
In this space, communication gains.
Letters, sounds, and grammar you’ll hone,
Find me where language becomes your own''', "answer": 217},
        
        {"question": "Two ships are sailing in the sea on the two sides of a lighthouse. The angle of elevation of the top of the lighthouse is observed from the ships are 30° and 45° respectively. If the lighthouse is 100 m high, the distance between the two ships is:", "answer": 273},
        
        {"question": '''I hold your fate in numbers and grades,
Where effort and time finally cascade.
With each sheet, a future unfolds,
Some dreams bright, others on hold.
I don't teach, I don’t test,
But in my hands, your progress rests.
Come to me when the term is done,
And see if the battle was lost or won''', "answer": 1},
        
        {"question": "A grocer has a sale of Rs. 6435, Rs. 6927, Rs. 6855, Rs. 7230 and Rs. 6562 for 5 consecutive months. How much sale must he have in the sixth month so that he gets an average sale of Rs. 6500?", "answer": 4991},
        
        {"question": '''In a realm where forces and laws intertwine,
And the essence of matter is meticulously defined.
Not a place where theories are simply discussed,
But where experiments test what’s deemed just.
With apparatus that measures the universe’s might,
And phenomena are explored both day and night.
Seek the lab where the principles of nature are tested,
And your clue lies where physics is bested''', "answer": 13},
    ],
    [   # Questions for Bot 2
        {"question": "A shopkeeper sells an article at a profit of 20%. If the cost price is Rs.250, what is the selling price", "answer": 300},
        
        {"question": '''In a realm where circuits spark and wires entwine,
The path to your clue, in this workshop,
 you'll find. Where volts and currents in harmony sway,
 Your destination's here, where they hold sway..''', "answer": 65},
        
        {"question": " Find the average value of current when the current that are equidistant are 4A, 5A and 6A", "answer": 5},
        
        {"question": '''In this quiet place, the network thrives,
Where unseen currents power lives.
Cables hum beneath a shielded door,
Housing secrets of the digital core.
Not a single spark nor a human sound,
Yet here, the world's data is found.
Seek the chamber where circuits meld,
The heart of the system, where tech is held.''', "answer": 114},
        
        {"question": " What is the approximate quantity of water in M7?", "answer": 45},
        
        {"question": '''In a realm where structures rise,
I test the strength beneath the skies.
From concrete to soil, my measures define,
How bridges and buildings align.
With tools and samples, I gauge the might,
Ensuring designs stand firm and right.
Seek the space where tests are run,
To see if your next clue has begun''', "answer": 110},
        
        {"question": " A block of mass 20 kg is placed on a frictionless horizontal surface. An applied force of 80 N is used to accelerate the block. Calculate the acceleration of the block.", "answer": 4},
        
        {"question": '''In a chamber where bytes and bits converge,
And digital signals silently surge.
Not a room where data is casually stored,
But a space where networks and servers are adored.
Lights blink rhythmically in a synchronized dance,
While data flows with an advanced trance.
Seek the vault where information is keenly housed,
And your clue lies where circuits are aroused.     ''', "answer": 114},
    ],
    [   # Questions for Bot 3
        {"question": '''The average of 20 numbers is zero. Of them, at the most, how many may be greater than zero?''', "answer": 19},

        {"question": '''In a realm where the smart and the connected meet,
Devices converse in signals discreet.
Here, networks weave through gadgets and code,
Turning data streams into a meaningful load.
Not a single wire is left unseen,
Where innovation and tech convene.
Seek the space where the digital world thrives,
And find your clue where IoT arrives       ''', "answer": 69},

        {"question": '''A car of mass 1,200 kg is moving with a constant acceleration of 3 m/s23 \, \text{m/s}^23m/s2. Calculate the net force acting on the car.''', "answer": 3600},

        {"question": '''In a realm where reality blurs and bends,
Where virtual landscapes and augmented realms blend.
Goggles and sensors create worlds anew,
Transforming your sight to experiences true.
In this space, the digital and real entwine,
Seek where imagination and tech align.
Find the lab where realities merge,
And your next clue will begin to emerge ''', "answer": 119},

        {"question": '''Three resistors, R1=40 Ω R2=60 ΩR3=120 ΩR are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 20},

        {"question": '''Where precision meets power in a seamless dance,
Machines carve wonders with automated finesse.
Metal and plastic, through commands they mold,
Transforming designs into shapes bold.
With tools that cut and spindles that spin,
Find where creation and accuracy begin.
Seek the lab where engineering’s art is found,
And uncover your clue where craftsmanship is crowned    ''', "answer": 68},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a realm where smart devices seamlessly connect,
And networks of sensors interact and reflect.
Not a place where circuits are simply laid,
But where data streams through the digital cascade.
From everyday objects to sophisticated tech,
This space turns signals into insights direct.
Find the lab where interconnected systems thrive,
And your clue lies where intelligent networks arrive     ''', "answer": 69},

    ],
    [   # Questions for Bot 4
        {"question": '''The ratio between the perimeter and the breadth of a rectangle is 5 : 1. If the area of the rectangle is 216 sq. cm, what is the length of the rectangle?''', "answer": 18},

        {"question": '''A Lab of Solutions        ''', "answer": 16},

        {"question": '''A car of mass 1,500 kg is moving with a constant acceleration of 4 m/s2. Calculate the net force acting on the car''', "answer": 6000},

        {"question": '''In a realm where rhetoric sharpens its edge,
And legal minds test their skills on the ledge.
Not a court of law, but a battleground of speech,
Where principles and arguments are within reach.
In this domain, precedents guide the way,
And every point made could sway the day.
Find the place where justice is staged,
And your next clue will be well engaged.     ''', "answer": 204},

        {"question": '''Three resistors, R1=30 Ω, R2=45 Ω, and R3=90 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 15},

        {"question": '''In a grand expanse where the flag waves high,
And the library and reception stand nearby.
A place where students gather and roam,
And the spirit of the college fi.        nds its home.
Not within walls, but where open skies greet,
Find the space where the Indian flag and pathways meet.
Seek the green expanse where pride does show,
And your next clue will be where the campus’s heart does grow.''', "answer": 5000},

        {"question": ''' What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a realm where currents and voltages dance,
And circuits transform with every chance.
Not a place where basic wiring is seen,
But where power systems are precisely keen.
Converters and regulators manage the flow,
Turning energy with a technical glow.
Seek the lab where electrical power is refined,
And your clue lies where electronics are aligned.    ''', "answer": 28},
    ],
    [   # Questions for Bot 5
        {"question": '''The diagonal of a rectangle is 41^1/2  cm and its area is 20 sq. cm. The perimeter of the rectangle must be:''', "answer": 18},

        {"question": '''In a space where justice and debate align,
Where aspiring advocates hone their design.
Not a court where verdicts are handed down,
But a stage where legal arguments are renowned.
Evidence is presented, and logic is clear,
In this arena where future lawyers steer.
Find the venue where the legal minds convene,
And your next clue is where courtroom dreams are seen.    ''', "answer": 204},

        {"question": '''A car of mass 1,000 kg is moving with a constant acceleration of 4 m/s2. Calculate the net force acting on the car''', "answer": 4000},

        {"question": '''In a domain where elements react and blend,
And compounds form as reactions transcend.
Not a kitchen where simple mixtures are made,
But a lab where scientific theories are played.
Beakers bubble and formulas collide,
Where precise measurements and tests reside.
Seek the room where chemical secrets unfold,
And your next clue will be where science is bold. ''', "answer": 16},

        {"question": '''Three resistors, R1=20 Ω, R2=50 Ω, and R3=75 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 12},

        {"question": '''In a space where currents flow and circuits meet,
Where power and electronics converge in a beat.
Not a simple wire, but a place where energy’s tamed,
And devices are tested and performance is named.
With transformers, diodes, and waves that rise,
Find the lab where electrical magic lies.
Seek the chamber where voltage and current align,
And your next clue will be where power design shines''', "answer": 28},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a room where language takes its form,
And eloquence is shaped through practice warm.
Not a classroom where literature is merely read,
But a space where spoken skills are finely spread.
Words and accents are honed to perfection,
Crafting communication with precise direction.
Find the lab where language is practiced with flair,
And your clue lies where spoken skills repair.    ''', "answer": 217},

    ],
    # Add more question sets for each bot...
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, questions):
    welcome_message = '''The first team to correctly solve all 5 questions and 4 riddles will be declared
winner of the treasure hunt.

Create a WhatsApp group that includes team members and one coordinator.
Add +917433070840.

Good luck to all participants, and let the hunt begin!

For locations without room numbers, use the following specific codes:

Workshop: 1000
Indoor Stadium/Games: 2000
Saraswati Mata Idol: 3000
Badminton Court: 4000
Central Lawn: 5000
Parking Lot: 6000
Indian Flag: 7000
Constitution of India: 8000
Reception: 9000
Canteen: 10000
Library:1100
Seminar Hall:1200
Admission Cell:1300
T and P Cell:1400
Reprography Section:1500'''
    await update.message.reply_text(welcome_message)
    await update.message.reply_text(questions[0]["question"])
    return QUESTION_STATES[0]

# Function to handle each question and check the answer
async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE, questions, current_question, next_state):
    try:
        answer = int(update.message.text)
        if answer == questions[current_question]["answer"]:
            if current_question < len(questions) - 1:
                await update.message.reply_text(questions[current_question + 1]["question"])
                return next_state
            else:
                end_message ='''#include <stdio.h>

int main() {
    printf("Trova l'app con un simbolo come una nota volante e invia il messaggio 'Abbiamo vinto' al 21D313297.\n");
return 0;
}

'''
                await update.message.reply_text(end_message)
                return ConversationHandler.END
        else:
            await update.message.reply_text(f"Incorrect! Try again: {questions[current_question]['question']}")
            return current_question
    except ValueError:
        await update.message.reply_text("Please enter a valid integer.")
        return current_question

# Error handler to log errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Define handlers for each question state dynamically based on the questions
def create_conversation_handler(questions):
    return ConversationHandler(
        entry_points=[CommandHandler('start', lambda update, context: start(update, context, questions))],
        states={
            QUESTION_STATES[0]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 0, QUESTION_STATES[1]))],
            QUESTION_STATES[1]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 1, QUESTION_STATES[2]))],
            QUESTION_STATES[2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 2, QUESTION_STATES[3]))],
            QUESTION_STATES[3]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 3, QUESTION_STATES[4]))],
            QUESTION_STATES[4]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 4, QUESTION_STATES[5]))],
            QUESTION_STATES[5]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 5, QUESTION_STATES[6]))],
            QUESTION_STATES[6]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 6, QUESTION_STATES[7]))],
            QUESTION_STATES[7]: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_question(update, context, questions, 7, ConversationHandler.END))],
        },
        fallbacks=[]
    )

# Function to run each bot
def run_bot(token, questions):
    application = Application.builder().token(token).build()
    
    # Add conversation handler for each bot
    conv_handler = create_conversation_handler(questions)
    application.add_handler(conv_handler)

    # Register the error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

# Main function to run multiple bots concurrently
def main():
    # List of your 30 bot tokens
    tokens = [
        '7462024671:AAHYDuXueKPgBDbU79UC8McP8J_sYuwKdWI',
        '6814394764:AAHqrOCNZB8it8r-jKLR39RZFCH5R3Tu2zE',
        '7223632152:AAF4jdymz6rcROWOGW1z9-vnUG2ScVvdVCc',
        '7283591225:AAH-tkvabbJIpe6a6eunNvtMZs-1bphw2xw',
        '7064459654:AAGkkyxBL3J1FNaRQ5RV9wnPiTwJtRvh4dw',
        '7433462511:AAGs-YbVM4NswKdporWiZKJzfSA8yqy0tLA',
        '7517160265:AAGeGqwZ3B795EEBl4CW87RLERGQpRrgCk8',
        '6776041552:AAGVKBh5iA40IFq6ll8OeUJ7rZ_cPZUE4XM',
        '7341123898:AAH4v4HFx_CtnnCdxBKqKtccJdNN2fTJ6pA',
        '7544876544:AAHiJVbdxqUt-Sp_e9tIzVWL0EefmJqMHi8',
        # Add tokens for all 30 bots here...
    ]

    # Create a process for each bot
    processes = []
    for i, token in enumerate(tokens):
        p = multiprocessing.Process(target=run_bot, args=(token, questions_list[i % len(questions_list)]))
        p.start()
        processes.append(p)

    # Keep the main process running
    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
