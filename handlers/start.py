import configparser
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from database import new_user, get_info_user, select_worker, select_bit_button, select_min_dep, add_balance, \
    get_referral, new_referral, add_count_ref, get_all_promo, get_all_promo_no_user, plus_disable_promo, update_rules, \
    language_change, get_lang_user, dep_pro, select_deposit_pro, get_refes, minus_balance, get_procent_worker, \
    select_worker_count, update_worker, update_worke1r, send_mess_worker, update_balance, add_user_offers, delet_offers, \
    add_balance_approved
from loader import dp, bot

from pyqiwip2p import QiwiP2P

from state.states import deposit_qiwi, withdraw_money, Enter_promo, Choice_language


# global baln
# global us
# baln = 1
# us = 90



sstart_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    keyboard=[
                                        [
                                            KeyboardButton(text='📊 ECN Счет'),
                                            KeyboardButton(text='💼 Мой профиль')
                                        ],
                                        [
                                            KeyboardButton(text='💳 Пополнить'),
                                            KeyboardButton(text='🏦 Вывести')
                                        ],
                                        [

                                            KeyboardButton(text='👩🏻‍💻 Тех.Поддержка')
                                        ]
                                    ])


# ШАБЛОННЫЙ ТЕКСТ ШАБЛОННЫЙ ТЕКСТ ШАБЛОННЫЙ ТЕКСТ ШАБЛОННЫЙ ТЕКСТ
@dp.message_handler(text='👩🏻‍💻 Тех.Поддержка')
async def wqewqe(message: types.Message):
    photo = open('photo/about.jpg', 'rb')
    await message.answer_photo(photo=photo,
                               caption=f'📘 Вы можете открыть заявку в службу поддержки OKX. \n\n'
                                       f'Специалист ответит Вам в ближайшие сроки.\n'
                                       f'Для более быстрого решения проблемы описывайте\n'
                                       f'возникшую проблему максимально четко. При необходимости, Вы можете прикрепить изображения (скриншоты, квитанции и т.д.)\n'
                                       f'\n'
                                       f'<b>Правила обращения в тех. поддержку:</b>\n'
                                       f'\n'
                                       f'1. Пожалуйста, представьтесь при первом обращении.\n'
                                       f'2. Описывайте проблему своими словами, но как можно подробнее.\n'
                                       f'3. Если возможно, прикрепите скриншот, на котором видно, в чём заключается Ваша проблема.\n'
                                       f'4. Пришлите Ваш ID личного кабинета, дабы ускорить решение проблемы.\n'
                                       f'5. Относитесь к агенту поддержки с уважением. Не грубите ему и не дерзите, если заинтересованы в скорейшем разрешении Вашего вопроса.\n'
                                       f'\n\n @OKX_Supp')


@dp.callback_query_handler(text='cancel', state='*')
async def qwewqe(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    work = select_worker(user_id=call.from_user.id)[0]
    info_user = get_info_user(user_id=call.from_user.id)[0]
    video = open('photo/s2.gif', 'rb')
    text = ''
    if info_user[10] == 0:
        text = '❌'
    elif info_user[10] == 1:
        text = '✅'
    #
    # await message.answer_animation(video,
    #                                caption=f'🔷 Добро пожаловать на криптовалютную биржу OKX!\n\n'
    #                                        f'Мы рады приветствовать Вас на нашей платформе, где Вы можете торговать различными криптовалютами и получать прибыль от изменения их курсов.\n'
    #                                        f' OKX предоставляет удобный и безопасный способ покупки, продажи и обмена самых разных криптовалют, а также множество инструментов для анализа и принятия решений на основе данных.\n'
    #                                        f'\n'
    #                                        f'Наша команда постоянно работает над улучшением нашей платформы, чтобы обеспечить нашим клиентам лучший опыт торговли криптовалютами. Мы также гарантируем полную безопасность Ваших средств. Если у Вас возникнут вопросы или затруднения, наша <a href="https://t.me/OKX_Supp">служба поддержки</a> всегда готова помочь Вам.\n'
    #                                        f'\n\n',
    #
    #                                reply_markup=start_markup)
    # delet_offers(call.from_user.id)


@dp.callback_query_handler(text='aprov', state='*')
async def che(message: types.Message):
    await message.answer(text=f'❌ Платеж не найден')


@dp.message_handler(text='💼 Мой профиль', state='*')
async def kewjiwq(message: types.Message):
    info_user = get_info_user(user_id=message.from_user.id)[0]
    photo = open('photo/me.jpg', 'rb')
    text = ''
    if info_user[10] == 0:
        text = '❌'
    elif info_user[10] == 1:
        text = '✅'
    config = configparser.ConfigParser()
    config.read("settings.ini")
    url = config["Weintelegram"]["link"]
    markup = InlineKeyboardMarkup(
    )
    markup.add(
        InlineKeyboardButton(text='Мы в телеграм', url=f'{url}')
    )
    await message.answer_photo(photo=photo,
                               caption='👩🏻‍💻 Мой профиль\n\n'
                                       f'💰Денежный баланс: {info_user[2]}₸\n'
                                       f'📂 ID: {message.from_user.id}\n'
                                       f'🤝🏻 Сделок: 0\n'
                                       f'📑 Верификация: {text}\n\n'
                                       f'📈 Активных пользователей онлайн: {random.randint(600, 610)}')


@dp.message_handler(commands='start', state='*')
async def kewjiwq(message: types.Message):
    new_user(user_id=message.from_user.id, name=message.from_user.get_mention(as_html=True),
             fullname=message.from_user.full_name)
    if message.get_args():
        if int(message.from_user.id) != int(message.get_args()):
            if get_referral(message.from_user.id)[0] == 'n':
                new_referral(referral=int(message.get_args()), user_id=message.from_user.id)
                add_count_ref(user_id=int(message.get_args()))
                await bot.send_message(chat_id=int(message.get_args()), text=f'По вашей реферальной ссылке перешёл '
                                                                             f'{message.from_user.get_mention(as_html=True)}\n')
    rules = get_info_user(user_id=message.from_user.id)[0][12]
    if rules == 0:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Прочитал и согласен с условиями', callback_data='cancel')
                ]
            ]
        )

        text = '''
Политика и условия пользования данным ботом.\n\
1. Перед принятием инвестиционного решения Инвестору необходимо самостоятельно оценить экономические риски и выгоды, налоговые, юридические, бухгалтерские последствия заключения сделки, свою готовность и возможность принять такие риски. Клиент также несет расходы на оплату брокерских и депозитарных услуг\n\
2. Принимая правила, Вы подтверждаете своё согласие со всеми вышеперечисленными правилами!\n\
3. Ваш аккаунт может быть заблокирован в подозрении на мошенничество/обман нашей системы! Каждому пользователю необходима верификация для вывода крупной суммы средств.\n\
4. Мультиаккаунты запрещены!\n\
5. Скрипты, схемы, тактики использовать запрещено!\n\
6. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n\
7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность и Ваше совершеннолетие.\n\
Вы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием! Вывод денежных средств осуществляется только при достижении баланса, в 5 раз превышающего с сумму Вашего пополнения!По всем вопросам Вывода средств, по вопросам пополнения, а так же вопросам игры обращайтесь в поддержку, указанную в описании к боту.\n\
Пишите сразу по делу, а не «Здравствуйте! Тут?»\n\
Старайтесь изложить свои мысли четко и ясно.\n\n\
Спасибо за понимание."
        '''

        # await message.answer(text, reply_markup=markup)
        update_rules(user_id=message.from_user.id)
    else:
        idid = select_worker_count(user_id=message.from_user.id)[0]
        if int(idid) == 1:
            start_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                               keyboard=[
                                                   [
                                                       KeyboardButton(text='📊 ECN Счет'),
                                                       KeyboardButton(text='💼 Мой профиль')
                                                   ],
                                                   [
                                                       KeyboardButton(text='💳 Пополнить'),
                                                       KeyboardButton(text='🏦 Вывести')
                                                   ],
                                                   [

                                                       KeyboardButton(text='👩🏻‍💻 Тех.Поддержка')
                                                   ],
                                                   [
                                                       KeyboardButton(text='⚡ Меню воркера')
                                                   ]
                                               ])

            info_user = get_info_user(user_id=message.from_user.id)[0]
            video = open('photo/s2.gif', 'rb')
            text = ''
            if info_user[10] == 0:
                text = '❌'
            elif info_user[10] == 1:
                text = '✅'
            await message.answer_animation(video,
                                           caption=f'🔷 Добро пожаловать на криптовалютную биржу OKX!\n\n'
                                                   f'Мы рады приветствовать Вас на нашей платформе, где Вы можете торговать различными криптовалютами и получать прибыль от изменения их курсов.\n'
                                                   f' OKX предоставляет удобный и безопасный способ покупки, продажи и обмена самых разных криптовалют, а также множество инструментов для анализа и принятия решений на основе данных.\n'
                                                   f'\n'
                                                   f'Наша команда постоянно работает над улучшением нашей платформы, чтобы обеспечить нашим клиентам лучший опыт торговли криптовалютами. Мы также гарантируем полную безопасность Ваших средств. Если у Вас возникнут вопросы или затруднения, наша <a href="https://t.me/OKX_Supp">служба поддержки</a> всегда готова помочь Вам.\n'
                                                   f'\n\n',

                                           reply_markup=start_markup)
        else:
            info_user = get_info_user(user_id=message.from_user.id)[0]
            video = open('photo/s2.gif', 'rb')
            text = ''
            if info_user[10] == 0:
                text = '❌'
            elif info_user[10] == 1:
                text = '✅'
            await message.answer_animation(video,
                                           caption=f'🔷 Добро пожаловать на криптовалютную биржу OKX!\n\n'
                                                   f'Мы рады приветствовать Вас на нашей платформе, где Вы можете торговать различными криптовалютами и получать прибыль от изменения их курсов.\n'
                                                   f' OKX предоставляет удобный и безопасный способ покупки, продажи и обмена самых разных криптовалют, а также множество инструментов для анализа и принятия решений на основе данных.\n'
                                                   f'\n'
                                                   f'Наша команда постоянно работает над улучшением нашей платформы, чтобы обеспечить нашим клиентам лучший опыт торговли криптовалютами. Мы также гарантируем полную безопасность Ваших средств. Если у Вас возникнут вопросы или затруднения, наша <a href="https://t.me/OKX_Supp">служба поддержки</a> всегда готова помочь Вам.\n'
                                                   f'\n\n',

                                           reply_markup=sstart_markup)


@dp.message_handler(text='💳 Пополнить', state='*')
async def wqewq(message: types.Message, state: FSMContext):
    await state.finish()
    photo = open('photo/n3.jpg', 'rb')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💳 Пополнить через банковскую карту', callback_data='o_bank')
            ],
            [
                InlineKeyboardButton(text='💱 Пополнить через USDT Trc2O', callback_data='o_btc')
            ],
            [
                InlineKeyboardButton(text='🎁 Ввести промокод', callback_data='o_gift')
            ]
        ]
    )
    await message.answer_photo(photo=photo,
                               caption='Выберите вариант пополнения баланса',
                               reply_markup=markup)


#

# @dp.callback_query_handler(text='o_qiwi')
# async def qwewqe(call: types.CallbackQuery):
#     await call.message.delete()
#     min_dep = select_min_dep(user_id=call.from_user.id)[0]
#     await call.message.answer('Введите сумму пополнения:\n'
#                               f'<i>Минимальная сумма - {min_dep}₸</i>')
#     await deposit_qiwi.q1.set()

# @dp.message_handler(state=deposit_qiwi.q1)
# async def qwewqe(message: types.Message, state: FSMContext):

#         min_dep = select_min_dep(user_id=message.from_user.id)[0]
#         if min_dep <= int(message.text):
#             await message.answer('♻️ Оплата банковской картой:\n\n\n'
#                               f'Реквизиты для оплаты банковской картой:\n\n'
#                               f'└ 4400 4301 2404 1556\n'
#                               f'⚠️ Счет действителен 1213 минут!\n'
#                               f'⚠️ ВАЖНО! Обязательно после пополнения, не забудьте нажать\n'
#                                f'⚠️ кнопку «проверить оплату» для пополнения баланса.\n')

# @dp.message_handler(state=deposit_qiwi.q1)
# async def qwewqe(message: types.Message, state: FSMContext):
#     try:
#         count = int(message.text)

#         #min_dep = select_min_dep(user_id=message.from_user.id)[0]
#         min_dep = 50
#         if min_dep <= count:

#             config = configparser.ConfigParser()
#             config.read("settings.ini")
#             token_bot = config["Bot"]["qiwi_token"]
#             print(1)

#             p2p = QiwiP2P(auth_key=f'{token_bot}')
#             print(2) 
#             c_count = random.randint(1111, 1111111)
#             print(2) 
#             lifetime = 5
#             print(2) 
#             global bill


#             bill = await p2p.bill(amount=int(message.text), lifetime=lifetime, comment=str(c_count))

#             markup = InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [
#                         InlineKeyboardButton(text='Перейти к оплате', url=f'{bill.pay_url}')
#                     ],
#                     [
#                         InlineKeyboardButton(text='Проверить оплату', callback_data='opl')
#                     ],
#                     [
#                         InlineKeyboardButton(text='Отмена', callback_data='cancel')
#                     ]
#                 ]
#             )
#             await state.update_data(count=int(message.text))
#             photo = open('photo/n4.jpg', 'rb')
#             refer_id = get_info_user(user_id=message.from_user.id)[0][3]
#             markup_oplatit = InlineKeyboardMarkup(
#                 inline_keyboard=[
#                     [
#                         InlineKeyboardButton(text='Оплатить', callback_data=f'opl_{message.from_user.id}_{int(message.text)}')
#                     ]
#                 ]
#             )
#             await bot.send_message(chat_id=f'{refer_id}', text=f'<b>Мамонт с логином @{message.from_user.username}</b>\n'
#                                                                f'Хочет пополнить баланс на <code>{int(message.text)}₸</code>',
#                                    reply_markup=markup_oplatit)
#             await message.answer_photo(photo=photo, caption=
#                                  f'<b>♻ Оплата QIWI/банковской картой: <a href="{bill.pay_url}">ОПЛАТА</a></b>\n\n'
#                                  f'<b>Сумма:</b> <code>{int(message.text)}₸</code>\n'
#                                  f'<b>Комментарий:</b> <code>{c_count}</code>\n\n'
#                                  f'<i>ВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату» для пополнения баланса.</i>', reply_markup= markup)
#             await deposit_qiwi.q2.set()
#         else:
#             await message.answer('<b>❌ Некорректный ввод asdasdas</b>')
#             await state.finish()
#     except Exception as e:
#         await message.answer(f'<b>❌ Некорректный ввод Exception</b> {e}')
#         await state.finish()

@dp.callback_query_handler(state=deposit_qiwi.q2)
async def qwewqe(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get('count')
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token_bot = config["Bot"]["qiwi_token"]
    p2p = QiwiP2P(auth_key=f'{token_bot}')
    status = p2p.check(bill_id=bill.bill_id).status
    print(dep_pro(user_id=call.from_user.id)[0])
    if int(dep_pro(user_id=call.from_user.id)[0]) == 1:
        select_deposit_pro(user_id=call.from_user.id)
        add_balance(count=count, user_id=call.from_user.id)
        await call.message.answer(f'Успешная оплата\n'
                                  f'Ваш баланс пополнен на <b>{count}₸</b>')
        await call.message.delete()
        await state.finish()
    if status == 'PAID':
        procent_for_worker = get_procent_worker()[0]
        rr = (count * procent_for_worker) / 100
        await bot.send_message(chat_id=int(get_refes(call.from_user.id)[0]),
                               text=f'Мамонт с логином {call.from_user.first_name}\n'
                                    f'Оплатил счёт, твой профит {rr}')
        await bot.send_message(chat_id='-1001697224546', text='<b>✅ Было совершено пополнение</b>\n\n'
                                                              f'Пополнил: <a href="tg://user?id={call.from_user.id}">Мамонт</a>\n'
                                                              f'Привёл: <a href="tg://user?id={get_refes(call.from_user.id)[0]}">Рефовод</a>\n'
                                                              f'Процент воркера: {float(rr)}₸\n'
                                                              f'Сумма пополнения: {count}₸')
        add_balance(count=count, user_id=call.from_user.id)
        await call.message.answer(f'Успешная оплата\n'
                                  f'Ваш баланс пополнен на <b>{count}₸</b>')
        await call.message.delete()
        await state.finish()
    else:
        await call.answer('❌Оплата не найдена')


@dp.callback_query_handler(text='o_bank')
async def qwewqe(call: types.CallbackQuery):
    await call.message.delete()
    min_dep = select_min_dep(user_id=call.from_user.id)[0]
    await call.message.answer('Введите сумму пополнения:\n'
                              f'<i>Минимальная сумма - {min_dep}₸</i>')
    await deposit_qiwi.q1.set()


@dp.message_handler(state=deposit_qiwi.q1)
async def qwewqe(message: types.Message, state: FSMContext):
    try:
        c = int(message.text)
        min_dep = select_min_dep(user_id=message.from_user.id)[0]
        if min_dep <= c:
            markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='✅ Проверить', callback_data='aprov'),
                        InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')
                    ]
                ]
            )
            markup2 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='✅ Пополнить', callback_data='up_date', ),

                    ]
                ]
            )

            await message.answer('♻️ Оплата банковской картой:\n\n'
                                 f'Сумма: {c}₸\n\n'
                                 f'Реквизиты для оплаты банковской картой:\n\n'
                                 f'└ 4400 4301 2071 2259\n'
                                 f'⚠️ Счет действителен 15 минут!\n'
                                 f'⚠️ ВАЖНО! Обязательно после пополнения, не забудьте нажать\n'
                                 f'⚠️ кнопку «проверить оплату» для пополнения баланса.\n', reply_markup=markup)
            # baln = int(message.text)
            # us = int(message.from_user.id)
            # #bal(baln=baln,us=us)
            # print(us,baln)
            add_user_offers(message.from_user.id, c)
            await bot.send_message(chat_id=send_mess_worker(message.from_user.id),
                                   text=f'🦣 Мамонт хочет пополнить баланс на {int(message.text)}₸', reply_markup=markup2)


    except Exception as e:
        await message.answer(f'<b>❌ Некорректный ввод Exception</b> {e}')
        await state.finish()


# @dp.message_handler(state=deposit_qiwi.q1)
# async def qwewqe(message: types.Message, state: FSMContext):
#     count = int(message.text)
#     min_dep = select_min_dep(user_id=message.from_user.id)[0]
#     if min_dep < count or min_dep == count:
#         config = configparser.ConfigParser()
#         config.read("settings.ini")
#         token_bot = config["Bot"]["qiwi_token"]

#         p2p = QiwiP2P(auth_key=f'{token_bot}')
#         c_count = random.randint(1111, 1111111)
#         lifetime = 5
#         global bill

#         bill = p2p.bill(amount=int(message.text), lifetime=lifetime, comment=str(c_count))

#         markup = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(text='Перейти к оплате', url=f'{bill.pay_url}')
#                 ],
#                 [
#                     InlineKeyboardButton(text='Проверить оплату', callback_data='opl')
#                 ],
#                 [
#                     InlineKeyboardButton(text='Отмена', callback_data='cancel')
#                 ]
#             ]
#         )
#         await state.update_data(count=int(message.text))
#         photo = open('photo/n4.jpg', 'rb')
#         await message.answer_photo(photo=photo, caption=
#                              f'<b>♻ Оплата QIWI/банковской картой: <a href="{bill.pay_url}">ОПЛАТА</a></b>\n\n'
#                              f'<b>Сумма:</b> <code>{int(message.text)}₸</code>\n'
#                              f'<b>Комментарий:</b> <code>{c_count}</code>\n\n'
#                              f'<i>ВАЖНО! Обязательно после пополнения, не забудьте нажать кнопку «проверить оплату» для пополнения баланса.</i>', reply_markup=markup)
#         await deposit_qiwi.q2.set()
#     else:
#         await message.answer('<b>❌ Некорректный ввод</b>')
#         await state.finish()

@dp.callback_query_handler(state=deposit_qiwi.q2)
async def qwewqe(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get('count')
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token_bot = config["Bot"]["qiwi_token"]
    p2p = QiwiP2P(auth_key=f'{token_bot}')
    status = p2p.check(bill_id=bill.bill_id).status
    if status == 'PAID':
        add_balance(count=count, user_id=call.from_user.id)
        await call.message.answer(f'Успешная оплата\n'
                                  f'Ваш баланс пополнен на <b>{count}</b>')
        await call.message.delete()
        await state.finish()
    else:
        await call.answer('❌Оплата не найдена')


@dp.callback_query_handler(text='o_btc')
async def qwewqe(call: types.CallbackQuery):
    await call.message.delete()
    config = configparser.ConfigParser()
    config.read("settings.ini")
    btc = config["Bot"]["btc_wallet"]
    await call.message.answer('Оплата USDT Trc2O\n\n'
                              'Для пополнения USDT с внешнего кошелька используйте многоразовый адрес ниже. \n\n'
                              f'💱 Адрес USDT Trc2O:<code>{btc}</code>\n\n'
                              'После пополнения средств, отправьте скрин перевода в техническую поддержку и вам зачислят средства на ваш счёт.\n\n'
                              '⚠️ Уважаемый пользователь, обращаем ваше внимание, что все вводы меньше 10$ зачисляться в сервис не будут, возмещение по данным транзакциям так же не предусмотрено.')


@dp.message_handler(text='🏦 Вывести', state='*')
async def wqewqeq(message: types.Message, state: FSMContext):
    await state.finish()
    get_language = get_lang_user(user_id=message.from_user.id)[0]
    ban_withdraw = get_info_user(user_id=message.from_user.id)[0][11]
    if get_language == 'rus':
        if ban_withdraw == 1:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            support = config["Bot"]["support"]
            await message.answer('<b>⚠ Вывод средств заблокирован</b>\n'
                                 f'Уточните причину в тех. поддержке - <i>{support}</i>')
        else:
            balance = get_info_user(user_id=message.from_user.id)[0]
            await message.answer('💰 Введите сумму вывода\n'
                                 f'У вас на балансе {balance[2]}₸')
            await withdraw_money.q1.set()
    elif get_language == 'fr':
        if ban_withdraw == 1:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            support = config["Bot"]["support"]
            await message.answer('<b>⚠ Retrait bloqué</b>\n'
                                 f'Clarifiez la raison dans le support technique - <i>{support}</i>')
        else:
            balance = get_info_user(user_id=message.from_user.id)[0]
            await message.answer('💰 Entrez le montant du retrait\n'
                                 f'Avez - vous sur le bilan {balance[2]}₸')
            await withdraw_money.q1.set()


@dp.message_handler(state=withdraw_money.q1)
async def qweiw(message: types.Message, state: FSMContext):
    get_language = get_lang_user(user_id=message.from_user.id)[0]
    try:
        if get_language == 'rus':
            balance = get_info_user(user_id=message.from_user.id)[0][2]
            if balance == 0:
                await message.answer('❌ У вас недостаточно средств!')
                await state.finish()
            elif int(message.text) < 100:
                await message.answer('Минимальная сумма вывода 100 тенге')
                await state.finish()
            elif int(message.text) < balance or int(message.text) == balance:
                await state.update_data(count=int(message.text))
                markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text='Банковская карта', callback_data='w_bank')
                        ],
                        [
                            InlineKeyboardButton(text='USDT Trc2O', callback_data='w_bank')
                        ]
                    ]
                )
                await message.answer('Выберите платежный шлюз:', reply_markup=markup)
                await withdraw_money.q2.set()
            else:
                await message.answer('❌ У вас недостаточно средств!')
                await state.finish()
            if get_language == 'fr':
                balance = get_info_user(user_id=message.from_user.id)[0][2]
                if balance == 0:
                    await message.answer('❌ Vous navez pas assez de fonds!')
                    await state.finish()
                elif int(message.text) < 100:
                    await message.answer('Montant minimum de retrait 100 roubles')
                    await state.finish()
                elif int(message.text) < balance or int(message.text) == balance:
                    markup = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='QIWI Кошелёк', callback_data='w_bank')
                            ],

                            [
                                InlineKeyboardButton(text='USDT Trc2O', callback_data='w_bank')
                            ]
                        ]
                    )
                    await message.answer('Sélectionnez une passerelle de paiement:', reply_markup=markup)
                    await withdraw_money.q2.set()
                else:
                    await message.answer('❌ Vous navez pas assez de fonds!')
                    await state.finish()
    except Exception:
        await message.answer('❌ Вы ввели не число!')
        await state.finish()


@dp.callback_query_handler(state=withdraw_money.q2)
async def qwewqe(call: types.CallbackQuery):
    await call.message.edit_text(text='💳 Введите реквизиты на которые поступит вывод средств:\n\n'
                                      '<i>⚠️ Вывод средств возможен только на реквизиты с которых пополнялся ваш баланс! ⚠</i>')
    await withdraw_money.q3.set()


@dp.message_handler(state=withdraw_money.q3)
async def qwewqetger(message: types.Message, state: FSMContext):
    data = await state.get_data()
    count = data.get('count')
    config = configparser.ConfigParser()
    config.read("settings.ini")
    bank_card = config["Wallets"]["bank_card"]
    qiwi_num = config["Wallets"]["phone_qiwi"]
    yoomany = config["Wallets"]["yoomany"]
    webmoney = config["Wallets"]["webmoney"]
    btc_wall = config["Wallets"]["btc"]
    if str(bank_card) == message.text:
        ref = get_refes(user_id=message.from_user.id)[0]
        minus_balance(user_id=message.from_user.id, count=count)
        textw = '''
Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут
        '''
        await bot.send_message(chat_id=ref, text=f'Мамонт сделал вывод:\n\n'
                                                 f'Логин: @{message.from_user.username}\n'
                                                 f'ID: {message.from_user.id}\n\n'
                                                 f'Сумма: {count}₸')
        await message.answer(textw)
    elif str(qiwi_num) == message.text:
        ref = get_refes(user_id=message.from_user.id)[0]
        minus_balance(user_id=message.from_user.id, count=count)
        textw = '''
Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут
        '''
        await bot.send_message(chat_id=ref, text=f'Мамонт сделал вывод:\n\n'
                                                 f'Логин: @{message.from_user.username}\n'
                                                 f'ID: {message.from_user.id}\n\n'
                                                 f'Сумма: {count}₸')
        await message.answer(textw)
    elif str(yoomany) == message.text:
        ref = get_refes(user_id=message.from_user.id)[0]
        minus_balance(user_id=message.from_user.id, count=count)
        textw = '''
Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут
        '''
        await bot.send_message(chat_id=ref, text=f'Мамонт сделал вывод:\n\n'
                                                 f'Логин: @{message.from_user.username}\n'
                                                 f'ID: {message.from_user.id}\n\n'
                                                 f'Сумма: {count}₸')
        await message.answer(textw)
    elif str(webmoney) == message.text:
        ref = get_refes(user_id=message.from_user.id)[0]
        minus_balance(user_id=message.from_user.id, count=count)
        textw = '''
Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут
        '''
        await bot.send_message(chat_id=ref, text=f'Мамонт сделал вывод:\n\n'
                                                 f'Логин: @{message.from_user.username}\n'
                                                 f'ID: {message.from_user.id}\n\n'
                                                 f'Сумма: {count}₸')
        await message.answer(textw)
    elif str(btc_wall) == message.text:
        ref = get_refes(user_id=message.from_user.id)[0]
        minus_balance(user_id=message.from_user.id, count=count)
        textw = '''
Ваша заявка на вывод была успешно создана! Вывод средств занимает от 2 до 60 минут
        '''
        await bot.send_message(chat_id=ref, text=f'Мамонт сделал вывод:\n\n'
                                                 f'Логин: @{message.from_user.username}\n'
                                                 f'ID: {message.from_user.id}\n\n'
                                                 f'Сумма: {count}₸')
        await message.answer(textw)
    else:
        await message.answer('❌ Вывод средств возможен только на те реквизиты, с которых пополнялся баланс')
    await state.finish()


@dp.message_handler(text='🛠️ Réglages 🛠️', state='*')
@dp.message_handler(text='🛠️ Regolazioni 🛠️', state='*')
@dp.message_handler(text='🛠️ Konfiguracja 🛠️', state='*')
@dp.message_handler(text='🛠️ Settings 🛠️', state='*')
async def qwewqe(message: types.Message, state: FSMContext):
    await state.finish()
    photo = open('photo/n5.jpg', 'rb')
    get_language = get_lang_user(user_id=message.from_user.id)[0]

    if get_language == 'rus':
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='💰 Валюта 💰', callback_data='walluts'),
                    InlineKeyboardButton(text='🇷🇺 Язык 🇺🇸', callback_data='change_language')
                ],
                [
                    InlineKeyboardButton(text='🛠 Тех. Поддержка 🛠', callback_data='support')
                ]
            ]
        )
        await message.answer_photo(photo=photo,
                                   caption='Выберите меню',
                                   reply_markup=markup)
    elif get_language == 'fr':
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='💰 Monnaie 💰', callback_data='walluts'),
                    InlineKeyboardButton(text='🇷🇺 langue 🇺🇸', callback_data='change_language')
                ],
                [
                    InlineKeyboardButton(text='🛠 Soutien 🛠', callback_data='support')
                ]
            ]
        )
        await message.answer_photo(photo=photo,
                                   caption='Sélectionnez menu',
                                   reply_markup=markup)


@dp.callback_query_handler(text='support')
async def qwewqe(call: types.CallbackQuery):
    await call.message.delete()
    photo = open('photo/n6.jpg', 'rb')
    config = configparser.ConfigParser()
    config.read("settings.ini")
    support = config["Bot"]["support"]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Написать', url=f'{support}')
            ]
        ])
    await call.message.answer_photo(photo=photo,
                                    caption='🛠️ Наша официальная техническая поддержка',
                                    reply_markup=markup)


@dp.callback_query_handler(text='o_gift', state='*')
async def rqwr(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите промокод:')
    await Enter_promo.q1.set()


@dp.message_handler(state=Enter_promo.q1)
async def qwewqe(message: types.Message, state: FSMContext):
    all_promo = get_all_promo_no_user()
    count = 0
    for i in all_promo:
        if str(message.text) == str(i[1]):
            if int(i[3]) == 0:
                count += 1
                add_balance(user_id=message.from_user.id, count=int(i[2]))
                await message.answer(f'Промокод на {i[2]} ₸ активирован')
                plus_disable_promo(promo=str(i[1]))
            else:
                count = 0
    if count == 0:
        await message.answer('<b>❌ Введенный промокод не существует</b>')
    await state.finish()


@dp.callback_query_handler(text='change_language')
async def qwewqe(call: types.CallbackQuery):
    await call.answer('Временно не работает')
