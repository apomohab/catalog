# start on 19-6-2019 2:PM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup import Catalog, Items, Base, User

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


# create user id
User1 = User(
    name="Saeed Shaban",
    email="Aposara.acp@gmail.com",
    picture='')
session.add(User1)
session.commit()


# catalog Front end
Catalog1 = Catalog(user_id=1, name='Front End')
session.add(Catalog1)
session.commit()


item1 = Items(
    user_id=1,
    title='html',
    details='HTML is the standard markup language for creating Web pages'
            ', HTML describes the structure of Web pages using markup,',
    category='frontend',
    catalog=Catalog1)
session.add(item1)
session.commit()

item2 = Items(
    user_id=1,
    title='css',
    details='CSS stands for Cascading Style Sheets, CSS describes how HTML'
            'elements are to be displayed on screen, paper, or in other media',
    category='frontend',
    catalog=Catalog1)
session.add(item2)
session.commit()


item3 = Items(
    user_id=1,
    title='javascript',
    details='JavaScript is the programming language of HTML and the Web,'
            ' paper, JavaScript is easy to learn.',
    category='frontend',
    catalog=Catalog1)
session.add(item3)
session.commit()

# catalog Back End

Catalog2 = Catalog(user_id=1, name='Back End')
session.add(Catalog2)
session.commit()


item1 = Items(
    user_id=1,
    title='python',
    details='Python is a programming language,'
            'ython can be used on a server'
            'to create web applications, Python is a popular'
            'programming language It was created'
            'by Guido van Rossum, and released in 1991.',
    category='backend',
    catalog=Catalog2)
session.add(item1)
session.commit()

item2 = Items(
    user_id=1,
    title='php',
    details='PHP is a server scripting '
            'language and a powerful'
            'tool for making dynamic'
            'and interactive Web pages',
    catalog=Catalog2)
session.add(item2)
session.commit()

item3 = Items(
    user_id=1,
    title='perl',
    details='The Perl Foundation is dedicated'
            'to the advancement of the Perl'
            'programming language through open discussion,'
            'collaboration, design, and code.',
    category='backend',
    catalog=Catalog2)
session.add(item3)
session.commit()


# catalog DataBase

Catalog3 = Catalog(user_id=1, name='DataBase')
session.add(Catalog3)
session.commit()


item1 = Items(
    user_id=1,
    title='Postgree',
    details='PostgreSQL is a powerful, open source object-relational'
            'database system with over 30 years of active'
            'development that has earned it a strong '
            'reputation for reliability, feature robustness,'
            'and performance. ',
    category='database',
    catalog=Catalog3)
session.add(item1)
session.commit()


item2 = Items(
    user_id=1,
    title='sqlite',
    details='SQLite is an embedded SQL database engine.'
            'Unlike most other SQL databases,'
            ' SQLite does not have a separate server process.',
    category='database',
    catalog=Catalog3)
session.add(item2)
session.commit()


# catalog FameWork

Catalog4 = Catalog(user_id=1, name='FrameWork')
session.add(Catalog4)
session.commit()

item1 = Items(
    user_id=1,
    title='Flask',
    details=' Flask is a microframework for Python based on Werkzeug,'
            ' Jinja 2 and good intentions. And before you ask: Its BSD . ',
    category='framework',
    catalog=Catalog4)
session.add(item1)
session.commit()

item2 = Items(
    user_id=1,
    title='Django',
    details='Django makes it easier to build better'
            'Web apps more quickly and with less code.',
    category='framework',
    catalog=Catalog4)
session.add(item2)
session.commit()


# Catalog CMS
Catalog5 = Catalog(user_id=1, name='CMS')
session.add(Catalog5)
session.commit()

item1 = Items(
    user_id=1,
    title='Wordpress',
    details=' This article is about the blogging software'
            'WordPress (WordPress.org).'
            ' For the blog host, see WordPress.com. ',
    category='cms',
    catalog=Catalog5)
session.add(item1)
session.commit()

item2 = Items(
    user_id=1,
    title='Blogger',
    details=' Create a beautiful blog that fits your style'
            'Choose from a selection of easy-to-use'
            ' templates all with flexible layouts and hundreds'
            ' of background images or design something new. ',
    category='cms',
    catalog=Catalog5)
session.add(item2)
session.commit()


print("OK...")
