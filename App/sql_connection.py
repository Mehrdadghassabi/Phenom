import sqlite3
from sqlite3 import Error
from gi.repository import Gio


def create_connection(database_file):
    """  
    create a database connection to a sqlite database

    :param database_file: path
    """
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        print(sqlite3.version)
    except Error:
        print(Error)

    return connection


def execute_query(connection, query):
    """
    this function execute a query

    :param connection: Connection
    :query: str
    """

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed succesfully")
    except Error as error:
        print(f"The error '{error}' occured")


drop_table="""
drop table if exists programs
"""

create_table="""
CREATE TABLE if not exists programs 
(
    name text not null,
    executable_file text text not null,
    primary key(name, executable_file)
)
"""

add_programs="""
insert into 
    programs (name, executable_file)
values
    ('{}', '{}')
"""



if __name__ == '__main__':
    connection = create_connection('programs_db.sqlite3')
    execute_query(connection, drop_table)
    execute_query(connection, create_table)
    all_apps = Gio.DesktopAppInfo.get_all()

    all_file = '''<aiml version="2.0" encoding="UTF-8">'''

    template = '''
    <category>
        <pattern>OPEN {}</pattern>
            <template>
                <random>
                   <li>Sure thing!</li>
                   <li>Right away, sir!</li>
                   <li>On it!</li>
                </random>
                <think><system>bash -c "gtk-launch {} &amp;> /dev/null &amp;"</system></think>
            </template>
    </category>

    <category>
        <pattern>OPEN {} *</pattern>
            <template>
                <random>
                   <li>Sure thing!</li>
                   <li>Right away, sir!</li>
                   <li>On it!</li>
                </random>
                <think><system>bash -c "gtk-launch {} &amp;> /dev/null &amp;"</system></think>
            </template>
    </category>
    '''

    for app in all_apps:
        execute_query(connection, add_programs.format(
            str(app.get_display_name()).lower().replace('&', 'and'),
        str(app.get_filename()).split('/')[-1]))

        all_file += template.format(
            str(app.get_display_name()).upper().replace('&', 'and'),
            str(app.get_filename()).split('/')[-1],
            str(app.get_display_name()).lower().replace('&', 'and'),
            str(app.get_filename()).split('/')[-1])
    
    all_file += '''</aiml>'''

    with open('launch_programs.aiml', 'w') as xml_file:
        n = xml_file.write(all_file)
        xml_file.close()