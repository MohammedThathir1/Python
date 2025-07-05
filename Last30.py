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

    [   # Questions for Bot 6
        {"question": '''What is the least number of squares tiles required to pave the floor of a room 15 m 17 cm long and 9 m 2 cm broad?''', "answer": 814},

        {"question": '''In a domain where forces and structures are tested,
And theories of strength are deeply invested.
Where concrete and soil yield their hidden might,
And experiments reveal their true light.
Not a construction site, but where science prevails,
Testing materials where the future entails.
Seek the chamber where resilience is explored,
And your clue will be where engineering is assured  ''', "answer": 110},

        {"question": '''A car of mass 1,100 kg is moving with a constant acceleration of 4 m/s2. Calculate the net force acting on the car''', "answer": 4400},

        {"question": '''In a space where harmony and rhythm blend,
Where melodies and notes gracefully extend.
Not a stage where performances are set,
But a room where musical skills are met.
Instruments and sheets create the sound,
Find where the echoes of music are found.
Seek the chamber where tunes come alive,
And your next clue will be where the music thrives  ''', "answer": 29},

        {"question": '''Three resistors, R1=24 Ω, R2=24 Ω, and R3=24 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 8},

        {"question": '''In a domain where elements react and fuse,
Where experiments reveal what we choose.
Not a simple mixture, but a space of precision,
Where compounds change in a scientific vision.
Beakers and flasks with bubbling schemes,
Where chemical reactions fulfill their dreams.
Seek the lab where transformations are planned,
And your clue will be where molecules expand        ''', "answer": 16},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a place where reactions bubble and blend,
And elements interact to transcend.
Not a simple setup where solutions are stirred,
But a lab where compounds are observed and inferred.
From acids to bases and mixtures that fizz,
Seek the room where chemical magic is.
Your clue lies where molecules dance in arrays,
And the secrets of matter are revealed through displays      ''', "answer": 16},
    ],
    [   # Questions for Bot 7
        {"question": '''The length of a rectangular plot is 20 metres more than its breadth. If the cost of fencing the plot @ 26.50 per metre is Rs. 5300, what is the length of the plot in metres?''', "answer": 60},

        {"question": '''In a space where reality and fantasy merge,
And digital landscapes with the real world converge.
Not a simple screen but a realm of depth,
Where augmented and virtual visions are kept.
Goggles and sensors craft experiences anew,
Find the lab where tech and imagination brew.
Seek the room where realities blend and play,
And your clue lies where the virtual and real sway     ''', "answer": 119},

        {"question": '''A car of mass 500 kg is moving with a constant acceleration of 4 m/s2. Calculate the net force acting on the car''', "answer": 2000},

        {"question": '''Where the end of a journey meets the score,
And the fruit of your labor is laid out in store.
Not a hall where lectures are delivered,
But a room where academic paths are considered.
In this space, the culmination of effort is displayed,
And your academic fate is precisely weighed.
Find the chamber where numbers and marks are unveiled,
And your clue will be where the results are detailed. ''', "answer": 1},

        {"question": '''Three resistors, R1=60 Ω, R2=60 Ω, and R3=120 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 24},

        {"question": '''A lab where you play with letters''', "answer": 217},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a realm where futures are carefully crafted,
And career paths are skillfully drafted.
Not a classroom where theories are taught,
But a space where job opportunities are sought.
Where resumes are polished and interviews are planned,
And connections for careers are skillfully manned.
Find the office where professional journeys start,
And your clue lies where careers take heart    ''', "answer": 1400},
    ],
    [   # Questions for Bot 8
        {"question": '''A tank is 25 m long, 12 m wide and 6 m deep. The cost of plastering its walls and bottom at 75 paise per sq. m, is: ''', "answer": 558},

        {"question": '''In a space where harmony and rhythm blend,
Where melodies and notes gracefully extend.
Not a stage where performances are set,
But a room where musical skills are met.
Instruments and sheets create the sound,
Find where the echoes of music are found.
Seek the chamber where tunes come alive,
And your next clue will be where the music thrives ''', "answer": 29},

        {"question": ''' A car of mass 500 kg is moving with a constant acceleration of 6 m/s2. Calculate the net force acting on the car''', "answer": 3000},

        {"question": '''In a domain where fluids twist and play,
And principles of motion flow each day.
Not a mere pool or stream you find,
But where forces and currents are intricately defined.
With experiments that reveal how fluids behave,
Find the lab where the study of flow is so brave.
Seek the place where turbulence and calm are explored,
And your clue lies where the science of dynamics is stored.   ''', "answer": 67},

        {"question": '''Three resistors, R1=90 Ω, R2=45 Ω, and R3=30 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination''', "answer": 15},

        {"question": '''In a realm where oversight and order align,
And the details of conduct are carefully defined.
Not a classroom where knowledge is imparted,
But a space where discipline and fairness are charted.
Here, rules and records are meticulously kept,
And where issues of integrity are adeptly swept.
Find the office where supervision is the key,
And your clue will be where responsibility meets authority   ''', "answer": 9},

        {"question": ''' What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a realm where circuits and current are crafted with care,
And voltage and resistance are precisely laid bare.
Not a space where wires simply connect,
But a workshop where electrical projects reflect.
With tools that measure and components that bind,
Seek the place where electrical designs are refined.
Your clue lies where the principles of power are explored,
And the workshop where connections are restored ''', "answer": 65},
    ],
    [   # Questions for Bot 9
        {"question": '''(112 x 54) = ?''', "answer": 70000},

        {"question": '''In a realm where oversight and order align,
And the details of conduct are carefully defined.
Not a classroom where knowledge is imparted,
But a space where discipline and fairness are charted.
Here, rules and records are meticulously kept,
And where issues of integrity are adeptly swept.
Find the office where supervision is the key,
And your clue will be where responsibility meets authority  ''', "answer": 9},

        {"question": '''A car of mass 200 kg is moving with a constant acceleration of 6 m/s2. Calculate the net force acting on the car''', "answer": 1200},

        {"question": '''In a place where words and accents evolve,
And communication skills are honed and resolved.
Not a library with books on the shelf,
But a lab where languages grow and delve.
With lessons and exercises that help you refine,
Find where linguistic proficiency aligns.
Seek the room where fluency is the aim,
And your clue lies where language training became.?''', "answer": 217},

        {"question": ''' Three resistors, R1=120 Ω, R2=60 Ω, and R3=40 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination''', "answer": 20},

        {"question": '''Where circuits and currents meet in a dance,
And electrical skills are given a chance.
Not a lab where theories alone are tested,
But a workshop where practical skills are invested.
With wires and tools that spark and engage,
Find the space where electrical projects take stage.
Seek where components and power are applied,
And your clue lies where hands-on skills reside  ''', "answer": 65},

        {"question": ''' What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a lab where data speaks and algorithms learn,
And models evolve from patterns discerned.
Not a space where computations are simply run,
But where artificial minds are finely spun.
From neural networks to predictive insights,
This room crafts intelligence with digital might.
Find where data and learning intersect,
And your clue lies where machine insights reflect''', "answer": 120},
    ],
    [   # Questions for Bot 10
        {"question": '''What least number must be added to 1056, so that the sum is completely divisible by 23 ?''', "answer": 2},

        {"question": '''In a space where outcomes and scores converge,
And the culmination of effort begins to emerge.
Not a classroom where lessons are imparted,
But a room where success and results are charted.
Where every number tells the tale of your strive,
And the records of achievement come alive.
Seek the place where academic fates are drawn,
And your clue lies where results are calmly withdrawn ''', "answer": 1},

        {"question": '''A car of mass 2000 kg is moving with a constant acceleration of 6 m/s2. Calculate the net force acting on the car.''', "answer": 12000},

        {"question": '''In a realm where data and algorithms intertwine,
And intelligent systems are crafted with design.
Not a library where knowledge is just read,
But a lab where machine learning is fed.
Models are trained and predictions made clear,
In a space where artificial minds appear.
Seek the room where insights and patterns are gleaned,
And your clue lies where intelligence is machine-seamed''', "answer": 120},

        {"question": '''Three resistors, R1=60 Ω, R2=30 Ω, and R3=20 Ω, are connected in parallel. Calculate the equivalent resistance of the parallel combination.''', "answer": 10},

        {"question": '''In a chamber where the art of argument is tried,
And legal minds test their skills with pride.
Not a courtroom where judges render their decree,
But a stage where aspiring lawyers draft their plea.
Precedents and arguments are skillfully debated,
In a space where courtroom strategies are created.
Find the arena where legal eloquence is honed,
And your clue lies where future lawyers’ skills are shown''', "answer": 204},

        {"question": '''What is the approximate quantity of water in M5?''', "answer": 60},

        {"question": '''In a realm where oversight and order prevail,
And vigilance ensures that rules never fail.
Not a classroom where lessons are taught in view,
But a space where discipline and guidance accrue.
Where fairness is monitored and conduct is key,
Find the office where academic integrity is seen.
Your clue lies where oversight is keenly enforced,
And the path to propriety is carefully sourced ''', "answer": 9},
    ],
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

        {"question": '''In a chamber where arguments and justice intertwine,
And mock trials are staged with precision fine.
Not a courtroom where real cases are tried,
But a setting where legal skills are applied.
With evidence and pleas expertly laid,
Seek where the theater of law is displayed.
Your clue lies where legal drama and debates are staged,
And the essence of justice is finely engaged ''', "answer": 204},
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

        {"question": '''In a space where structures and forces are tested with might,
And the strength of materials comes to light.
Not a field where buildings rise from ground,
But a lab where civil principles are profound.
From stress tests to structural designs,
Find the lab where engineering meets the lines.
Your clue lies where the laws of construction are tried,
And the resilience of materials is verified ''', "answer": 110},
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

        {"question": '''In a haven where melodies and harmonies converge,
And the soul of music begins to emerge.
Not a stage where performances are given their due,
But a room where sound is meticulously pursued.
Instruments rest where notes softly play,
Crafting tunes in a harmonious array.
Find the space where musical dreams are spun,
And your clue lies where the art of music is won''', "answer": 29},
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

        {"question": '''In a quiet space where outcomes are revealed,
And the efforts of students are officially sealed.
Not a classroom where lessons are learned,
But a place where results are meticulously discerned.
From grades to feedback, all is laid bare,
Find the room where academic fates are declared.
Your clue lies where success and effort align,
And results are distributed with precision fine''', "answer": 1},
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

        {"question": '''In an open expanse where colors proudly fly,
And the symbol of a nation reaches the sky.
Not a hall where events are held with cheer,
But a place where the flag waves in clear.
Where the heart of the campus stands proud and free,
Find the lawn where national pride you’ll see.
Your clue lies where the tricolor soars high,
And the space of unity beneath it lie ''', "answer": 5000},
    ],
    # Add more question sets for each bot...
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, questions):
    welcome_message = '''The first team to correctly solve all 5 questions and 4 riddles will be declared
winner of the treasure hunt.

Create a WhatsApp group that includes team members and one coordinator.
Add +916350605152.

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
        '7237783336:AAHwf3VJ1zJhrP6t3HOBFfrNUTydvzwwzMI',
        '7528335890:AAGsO655C1oy-xhfbw8AYBsyt7LI6Q1aIxs',
        '7233201654:AAEkHDFsihwu0cX7pL5b4pEPagK3uwSPMg0',
        '7350040796:AAEh7j6ZxJZFPKjTjjAsEE4HcZZnDTWUcpk',
        '7255872823:AAEsvAd09xi6v9muQf-E4jo8Ykr9rNwbyVw',
        '7274900378:AAHOr_r3vrYRvveoHmNzqGVQLkdwHpQ13gc',
        '7169945897:AAF5tlR8yh4r4ffbzhlKarEglrREpccHU1o',
        '7527814069:AAHewGdIDCUEXwpro1qVOn8O7juEtQ8ZKtM',
        '7225113628:AAHT1PbGF80hjoSD_RMmVyG5n2WTWh6hMTU',
        '7540595051:AAF5xo816M_RTEfC4QZaQ0ZLdbSaIrf9IF8',
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
