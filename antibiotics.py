import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

with open('C:/Users/Oleg_Buhtin/Desktop/token AP.txt', 'r') as key:
    token=key.read()

#подключение бота
bot = telebot.TeleBot(token)


users={}

dose={'over':2, 
      'low':1}


metronidazol={'upper':'',
             'biliar':'',
             'intestinum':', метронидазол 500 мг в/в',
             'colorectal':', метронидазол 500 мг в/в',
             'hernia':'',
             'gyne':'',
             'cranio':'',
             'trauma':'',
             'uro':'',
             'urina':'',
             'non_uro':'',
             'cysto':'',
             'prostata':''}

try:
    begin=telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    begin_type=telebot.types.KeyboardButton('/start')
    begin.add(begin_type)

    start_keyboard=InlineKeyboardMarkup(row_width=1)
    start_button=InlineKeyboardButton('Определить тактику', callback_data='start')
    start_keyboard.add(start_button)

    allergy=InlineKeyboardMarkup(row_width=1)
    allergy_y=InlineKeyboardButton('Да', callback_data='allergy_y')
    allergy_n=InlineKeyboardButton('Нет', callback_data='allergy_n')
    allergy.add(allergy_y, allergy_n)

    weight=InlineKeyboardMarkup(row_width=1)
    weight_over=InlineKeyboardButton('Больше 80 кг', callback_data='over')
    weight_low=InlineKeyboardButton('Меньше 80 кг', callback_data='low')
    weight.add(weight_over, weight_low)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        global users
        users[message.from_user.id]={}
        print(users)
        bot.send_message(message.chat.id, 'Привет! Я бот для определения тактики периоперационной антибиотикопрофилактики.', reply_markup=start_keyboard)

    @bot.callback_query_handler(func=lambda c: c.data=='start')
    def system_ab(call):
        global users
        if users[call.from_user.id]=={}:
            users[call.from_user.id]['score']=0
            print(users)
            system_therapy=InlineKeyboardMarkup(row_width=2)
            system_y=InlineKeyboardButton('Да', callback_data='system_y')
            system_no=InlineKeyboardButton('Нет', callback_data='system_n')
            system_therapy.add(system_y, system_no)
            bot.answer_callback_query(call.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Получает ли сейчас пациент системную антибиотикотерапию?', reply_markup=system_therapy)

    @bot.callback_query_handler(func=lambda c: c.data in ['system_y', 'system_n'])
    def patient_health(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('system_therapy') is None:
            users[call.from_user.id]['system_therapy']=call.data
            patient=InlineKeyboardMarkup(row_width=1)
            good_health=InlineKeyboardButton('Здоров/нетяжёлое заболевание', callback_data='patient_good')
            bad_disease=InlineKeyboardButton('Тяжёлое сопутствующее заболевание', callback_data='bad_disease')
            patient.add(good_health, bad_disease)
            bot.answer_callback_query(call.id)
            if call.data=='system_y':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Пациенту не требуется дополнительная периоперационная профилактика', reply_markup=None)
            elif call.data=='system_n':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Есть ли у пациента системные заболевания?', reply_markup=patient)

    @bot.callback_query_handler(func=lambda c: c.data in ['patient_good', 'bad_disease'])
    def operation_type(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('health') is None:
            users[call.from_user.id]['health']=call.data
            bot.answer_callback_query(call.id)
            if call.data=='bad_disease':
                users[call.from_user.id]['score']+=1
            print(users)
            operation=InlineKeyboardMarkup(row_width=1)
            clear=InlineKeyboardButton('Чистая', callback_data='clear')
            almost_clear=InlineKeyboardButton('Условно-чистая', callback_data='almost clear')
            contaminated=InlineKeyboardButton('Контаминированная', callback_data='contaminated')
            dirty=InlineKeyboardButton('Грязная', callback_data='dirty')
            operation.add(clear, almost_clear, contaminated, dirty)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Какая операция предстоит пациенту?\n'
                                  'Чистая - плановая, без вскрытия просвета полых органов, при невоспалительных заболеваниях\n'
                                  'Условно-чистая - со вскрытием просвета дыхательных, пищеварительных, мочевыводящих и половых путей, грыжесечение (в том числе с установкой сетчатого импланта), с необходимостью постановки дренажей\n'
                                  'Контаминированная - в условиях воспалительного процесса, со вскрытием просвета полых органов, обработка свежих травматических ран\n'
                                  'Грязная - при гнойно-воспалительных процессах, некрозах, перитоните, перфорации полых органов, наличии инородных тел', reply_markup=operation)

    @bot.callback_query_handler(func=lambda c: c.data in ['clear', 'almost clear', 'contaminated', 'dirty'])
    def operation_time(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('sterility') is None:
            users[call.from_user.id]['sterility']=call.data
            bot.answer_callback_query(call.id)
            if call.data=='almost clear':
                users[call.from_user.id]['score']+=1
            elif call.data in ['contaminated', 'dirty']:
                users[call.from_user.id]['score']+=2
            print(users)
            time=InlineKeyboardMarkup(row_width=1)
            more_then_hour=InlineKeyboardButton('Больше 1 часа', callback_data='>1 hour')
            less_then_hour=InlineKeyboardButton('Меньше 1 часа', callback_data='<1 hour')
            time.add(more_then_hour, less_then_hour)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Предполагаемая продолжительность операции?', reply_markup=time)

    @bot.callback_query_handler(func=lambda c: c.data in ['>1 hour', '<1 hour'])
    def need(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('time') is None:
            users[call.from_user.id]['time']=call.data
            bot.answer_callback_query(call.id)
            if call.data=='>1 hour':
                users[call.from_user.id]['score']+=1
            print(users)
            if users[call.from_user.id]['score']>=2:
                region=InlineKeyboardMarkup(row_width=1)
                gi=InlineKeyboardButton('Операция на желудочно-кишечном тракте', callback_data='GI')
                urology=InlineKeyboardButton('Урологическая операция', callback_data='uro')
                gyne=InlineKeyboardButton('Гинекологическая операция', callback_data='gyne')
                etr=InlineKeyboardButton('Операция на ЛОР-органах', callback_data='etr')
                cranio=InlineKeyboardButton('Краниотомия', callback_data='cranio')
                trauma=InlineKeyboardButton('Травматологическая операция', callback_data='trauma')
                region.add(gi, urology, gyne, etr, cranio, trauma)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Требуется периоперационная антибиотикопрофилактика. Укажите область выполнения операции', reply_markup=region)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Периоперационная антибиотикопрофилактика не требуется.', reply_markup=None)

    @bot.callback_query_handler(func=lambda c: c.data=='GI')
    def gastrointestinal_organ(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('general_location') is None:
            users[call.from_user.id]['general_location']=call.data
            bot.answer_callback_query(call.id)
            organ=InlineKeyboardMarkup(row_width=1)
            upper=InlineKeyboardButton('Пищевод, желудок,\n'
                                        '12-перстная кишка', callback_data='upper')
            biliar=InlineKeyboardButton('Печень,\n'
                                         'поджелудочная железа', callback_data='biliar')
            intestinum=InlineKeyboardButton('Тонкая кишка', callback_data='intestinum')
            colorectal=InlineKeyboardButton('Толстая/прямая кишка,\n'
                                             'аппендэктомия', callback_data='colorectal')
            hernia=InlineKeyboardButton('Грыжесечение', callback_data='hernia')
            organ.add(upper, biliar, intestinum, colorectal, hernia)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Требуется проведение периоперационной антибиотикопрофилактики. Укажите область выполнения хирургической операции', reply_markup=organ)

    @bot.callback_query_handler(func=lambda c: c.data in ['upper', 'biliar', 'intestinum', 'colorectal', 'hernia', 'gyne', 'prostata']) 
    def gastrointestinal_allergy(call):
        global users
        flag=users[call.from_user.id]    
        if flag.get('location') is None:
            users[call.from_user.id]['location']=call.data
            bot.answer_callback_query(call.id)
            print(users)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Есть ли у пациента аллергия на цефазолин?', reply_markup=allergy)
        

    @bot.callback_query_handler(func=lambda c: c.data in ['allergy_y', 'allergy_n'])
    def gastrointestinal_weight(call):
        global users
        flag=users[call.from_user.id]    
        if flag.get('allergy') is None:
            users[call.from_user.id]['allergy']=call.data
            bot.answer_callback_query(call.id)
            if call.data=='allergy_y':
                if users[call.from_user.id]['location']=='prostata':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Необходимо ввести ципрофлоксацин 400 мг в/в капельно за 2 часа до кожного разреза.\n'
                    'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести ципрофлоксацин 400 мг в/в капельно через 12 часов.', reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Необходимо ввести ципрофлоксацин 400 мг в/в капельно + метронидазол 500 мг в/в за 2 часа до кожного разреза.\n'
                    'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести ципрофлоксацин 400 мг в/в капельно + метронидазол 500 мг в/в через 12 часов.', reply_markup=None)
            elif call.data=='allergy_n':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Масса пациента?', reply_markup=weight)

    @bot.callback_query_handler(func=lambda c: c.data in ['over', 'low'])
    def gastrointestinal_cephazolin(call):
        global dose, metronidazol, users
        flag=users[call.from_user.id]    
        if flag.get('patient_weight') is None:
            users[call.from_user.id]['patient_weight']=call.data
            bot.answer_callback_query(call.id)
            print(users)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Необходимо ввести цефазолин {dose[users[call.from_user.id]["patient_weight"]]} г в/в капельно{metronidazol[users[call.from_user.id]["location"]]} за 30 минут до кожного разреза.\n'
            f'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести цефазолин {dose[users[call.from_user.id]["patient_weight"]]} г в/в капельно через 4 часа.', reply_markup=None)


    @bot.callback_query_handler(func=lambda c: c.data in ['cranio', 'trauma', 'urina', 'non_uro', 'cysto']) 
    def trauma_allergy(call):
        global users
        flag=users[call.from_user.id]    
        if flag.get('location') is None:
            users[call.from_user.id]['location']=call.data
            bot.answer_callback_query(call.id)
            print(users)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Масса пациента?', reply_markup=weight)
    

    @bot.callback_query_handler(func=lambda c: c.data=='etr') 
    def etr_allergy(call):
        global users
        flag=users[call.from_user.id]    
        if flag.get('location') is None:
            users[call.from_user.id]['location']=call.data
            bot.answer_callback_query(call.id)
            print(users)
            allergy_amox=InlineKeyboardMarkup(row_width=1)
            allergy_amox_y=InlineKeyboardButton('Да', callback_data='allergy_amox_y')
            allergy_amox_n=InlineKeyboardButton('Нет', callback_data='allergy_amox_n')
            allergy_amox.add(allergy_amox_y, allergy_amox_n)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Есть ли у пациента аллергия на амоксицилин/клавулановую кислоту?', reply_markup=allergy_amox)

    @bot.callback_query_handler(func=lambda c: c.data in ['allergy_amox_y', 'allergy_amox_n'])
    def etr_tactic(call):
        global users
        flag=users[call.from_user.id]    
        if flag.get('allergy_amox') is None:
            users[call.from_user.id]['allergy_amox']=call.data
            bot.answer_callback_query(call.id)
            if call.data=='allergy_amox_y':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Необходимо ввести клиндамицин 600 мг в/в капельно за 30 мин до кожного разреза.\n'
                'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести клиндамицин 600 мг в/в капельно через 5 часов.', reply_markup=None)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Необходимо ввести амоксициллин/клавулановую кислоту 1,2 г в/в капельно за 30 мин до кожного разреза.\n'
                'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести амоксициллин/клавулановую кислоту 1,2 г в/в капельно через 2 часа.', reply_markup=None)

    @bot.callback_query_handler(func=lambda c: c.data=='uro') 
    def uro_location(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('general_location') is None:
            users[call.from_user.id]['general_location']=call.data
            bot.answer_callback_query(call.id)
            organ=InlineKeyboardMarkup(row_width=1)
            urina=InlineKeyboardButton('Операции на мочевыводящих путях', callback_data='urina')
            prostata=InlineKeyboardButton('Операции на предстательной железе', callback_data='prostata')
            biopsia=InlineKeyboardButton('Трансректальная биопсия\n'
                                          'простаты', callback_data='biopsia')
            non_uro=InlineKeyboardButton('Вмешательства не на\n'
                                          'мочевых путях', callback_data='non_uro')
            cysto=InlineKeyboardButton('Цистоскопия, уродинамические исследования', callback_data='cysto')
            organ.add(urina, prostata, biopsia, non_uro, cysto)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Требуется периоперационная антибиотикопрофилактика. Укажите область выполнения операции', reply_markup=organ)


    @bot.callback_query_handler(func=lambda c: c.data=='biopsia') 
    def uro_biopsia(call):
        global users
        flag=users[call.from_user.id]
        if flag.get('operation') is None:
            users[call.from_user.id]['operation']=call.data
            bot.answer_callback_query(call.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Необходимо ввести ципрофлоксацин 400 мг в/в капельно + метронидазол 500 мг в/в за 2 часа до кожного разреза.\n'
            'При продолжительности операции более 3 часов или развитии интраоперационных осложнений следует ввести ципрофлоксацин 400 мг в/в капельно + метронидазол 500 мг в/в через 12 часов.', reply_markup=None)


    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, "Команда не распознана.\n/start - начать определение тактики периоперационной профилактики", reply_markup=begin)

except:
    pass

bot.polling()