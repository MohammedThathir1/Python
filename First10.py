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
        
        {"question": '''I bear a wheel that never turns,
In stillness, its wisdom burns.
Above, the warmth of a blazing dawn,
Below, fertile life is drawn.
In between, calm skies reside,
Where unity and peace abide.
I do not walk, I do not speak,
But those who seek freedom, me they seek.''', "answer": 7000},
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
        
        {"question": '''I'm the first stop on your special day,
 Where greetings and smiles come your way.
 Guests arrive with joy and cheer,
 What am I, where is the celebration near? ''', "answer": 9000},
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

        {"question": '''In a realm where futures are carefully planned,
And paths to education are mapped and scanned.
Not a classroom where lessons are taught,
But a space where enrollment and records are sought.
Applications and queries are processed with care,
And the journey to join begins here, laid bare.
Find the office where your academic start is revealed,
And your clue lies where admission steps are sealed.    ''', "answer": 1400},

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

        {"question": '''In a space where Newton's laws flow and bend,
And fluid behavior’s mysteries never end,
Not a river or sea, but where precision is key,
To understand how substances move with glee.
Where pressures and velocities intertwine,
And experiments test the forces that align.
Seek the chamber where the unseen currents play,
And your next clue will be found where fluid dynamics sway   ''', "answer": 67},
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

        {"question": '''In a tome where the nation’s principles are bound,
Laws and rights in profound pages are found.
Not a scroll, nor a simple guide,
But a book where democracy’s essence resides.
It details the framework that governs the land,
And outlines the rights that we all understand.
Seek where the foundation of justice and order is penned,
And your clue lies where the nation’s laws blend.      ''', "answer": 8000},

    ],
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

        {"question": '''In a space where aromas fill the air,
And hungry students find a moment to share.
Not a classroom where knowledge is taught,
But a place where meals and snacks are sought.
With tables and trays, and dishes that delight,
Find the spot where you can grab a bite.
Seek where the scent of food does beckon,
And your clue will be where the canteen is reckon. ''', "answer": 1000},
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

        {"question": '''In a domain where automobiles line up with care,
And the order of rows is beyond compare.
Not a place where engines are turned or tuned,
But a vast expanse where parked vehicles are strewn.
This open field, marked with lines and slots,
Holds the key where your next clue is sought.
Find where cars gather and drivers align,
And your answer is where parked cars intertwine     ''', "answer": 6000},
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

        {"question": '''Where sparks fly and metal meets might,
And tools shape creations with skillful delight.
Not a design room where plans are laid,
But a space where hands and machines have played.
Here, materials are forged and crafted with care,
And engineering marvels are created with flair.
Seek the domain where precision and power blend,
And your clue will be where craftsmanship extends.  ''', "answer": 1000},
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

        {"question": '''In a realm where copies and prints are refined,
And documents and images are precisely aligned.
Not a place where originals are kept in sight,
But where duplication and reproduction take flight.
With machines that replicate each page and line,
Find the section where every print is designed.
Seek the area where your documents are reborn,
And your clue lies where copies are form   ''', "answer": 1500},
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

        {"question": '''In a space where paddles and balls engage in flight,
And quick reflexes determine who’s right.
Not a court where grand games are staged,
But a table where rallies and spins are waged.
With serves that spin and strikes that bounce,
Find where the game of precision counts.
Seek the table where speed and skill combine,
And your clue lies where the ball’s path aligns.  ''', "answer": 2000},
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
        '7129077929:AAFucRhBMQvHQIeCbw9Vjx0n2YzPzPe2pAM',
        '6353969175:AAGZ1qyiaRz3Ew81HFw66wWN543KKxfaf2g',
        '7506388981:AAGMM6xuFV1u8lWHjU4w2d1TwKEVDTZcpLg',
        '7195944921:AAEb5HmkAkEE-LwaArv0L9HvJEAB1O5_Jco',
        '7071746995:AAGI1UE3rBIOADBPEMdyeM0deTljG4EvEbw',
        '7279854290:AAGwGxw7gV7Ghu_8dUQ5Mo4zGkjTlwdk6uQ',
        '7282412184:AAEKk4xS_cjWZxhhr9RjECwLlEE7rBPOkOg',
        '7022597688:AAEjvCJGG3WI8xvN_HLogm8i-HgpJWXLe0k',
        '7453543610:AAFMbgYoVLOEAbQiKZHUPUUuV2xSLxjXoO0',
        '7323516440:AAHVwnZp31Ci8GY4SHhhWWA9wGyvA6RmhXg',
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
