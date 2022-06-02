from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.padding import Padding
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import requests
import psutil
from datetime import datetime
import random
import time
import json
import sys
import re

__VERSION__ = 2.5

# adjust console size with your own values before using
console = Console(height=66)  # full size: height: 66, width: 240 (ASUS VE248)


class Dashboard:

    def __init__(self):
        self.boot_time = datetime.fromtimestamp(psutil.boot_time()).replace(microsecond=0)
        self.pattern_open, self.pattern_inprogress, self.pattern_closed = re_patterns()
        self.daily_data = None
        self.general_data = None
        self.notes_data = None
        self.score_prio = str()
        self.score_total = str()
        self.layout = None
        self.layout_config()

    def render_board(self):
        self.update_data()
        console.clear()
        console.print(self.layout)

    def update_data(self):
        time_1 = self.get_data('daily')
        time_2 = self.get_data('general')
        time_3 = self.get_notes()
        self.get_score()

        self.render_header()
        self.render_table_daily()
        self.render_table_general()
        self.render_notes()
        self.render_footer(time_1 + time_2 + time_3)

    # initialize dashboard
    def layout_config(self):
        self.layout = Layout()
        self.layout.split_column(
            Layout(name='top', size=3),
            Layout(name='content'),
            Layout(name='bottom', size=3),
        )

        self.layout['top'].split_row(
            Layout(name='top_left'),
            Layout(name='top_mid'),
            Layout(name='top_right'),
        )

        self.layout['content'].split_column(
            Layout(name='content_top'),
            Layout(name='content_bottom'),
        )
        self.layout['content_top'].split_row(
            Layout(name='left'),
            Layout(name='right'),
        )
        self.layout['left'].split_column(
            Layout(name='left_upper', size=11),
            Layout(name='left_lower'),
        )
        DAILY = r'''██████   █████  ██ ██      ██    ██ 
██   ██ ██   ██ ██ ██       ██  ██  
██   ██ ███████ ██ ██        ████   
██   ██ ██   ██ ██ ██         ██    
██████  ██   ██ ██ ███████    ██    '''
        self.layout['left_upper'].update(
            Align(Padding(Panel(DAILY, box=box.SQUARE, style='white', border_style='black'), (4, 0, 0, 0)),
                  align='center'))

        self.layout['right'].split_column(
            Layout(name='right_upper', size=11),
            Layout(name='right_lower'),
        )
        GENERAL = r''' ██████  ███████ ███    ██ ███████ ██████   █████  ██
██       ██      ████   ██ ██      ██   ██ ██   ██ ██    
██   ███ █████   ██ ██  ██ █████   ██████  ███████ ██    
██    ██ ██      ██  ██ ██ ██      ██   ██ ██   ██ ██     
 ██████  ███████ ██   ████ ███████ ██   ██ ██   ██ ███████'''
        self.layout['right_upper'].update(
            Align(Padding(Panel(GENERAL, box=box.SQUARE, style='white', border_style='black'), (4, 0, 0, 0)),
                  align='center'))

        self.layout['content_bottom'].split_column(
            Layout(name='content_bottom_title', size=8),
            Layout(name='content_bottom_notes'),
        )
        NOTES = r'''
 _   _  ___ _____ _____ ____  
| \ | |/ _ |_   _| ____/ ___| 
|  \| | | | || | |  _| \___ \ 
| |\  | |_| || | | |___ ___) |
|_| \_|\___/ |_| |_____|____/ 
            
'''
        self.layout['content_bottom_title'].update(
            Align(Panel(NOTES,
                        box=box.SQUARE,
                        border_style='black'
                        ),
                  align='center'
                  )
        )

        self.layout['bottom'].split_row(
            Layout(name='bottom_left'),
            Layout(name='bottom_mid'),
            Layout(name='bottom_right'),
        )

    def render_header(self):
        self.layout['top_left'].update(Align(Panel(self.score_prio,
                                                   box=box.SQUARE),
                                             align='center'))
        self.layout['top_mid'].update(Align(Panel(self.gen_logo(),
                                                  box=box.SQUARE,
                                                  style='bright_black'),
                                            align='center'))
        self.layout['top_right'].update(Align(Panel(self.score_total,
                                                    box=box.SQUARE),
                                              align='center'))

    def gen_logo(self):
        """
        Returns STARBOARD written logo with letters in randomized colors.
        Selects from 15 terminal standard colors (excluding black).
        """
        COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
                  'bright_black', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
                  'bright_cyan', 'bright_white']
        logo = list('STARBOARD')
        for letter in logo:
            i = logo.index(letter)
            logo = logo[:i] + [f'[{random.choice(COLORS)}]{letter}'] + logo[i + 1:]
        return ' '.join(logo)

    def render_table_daily(self):
        table = Table(box=box.SQUARE,
                      leading=True, highlight=False,
                      header_style='black on white',
                      style='black')
        for column in self.daily_data['row_0']:
            table.add_column(column, justify='center')
        # check that the table contains rows below the header row
        if len(self.daily_data) > 1:
            for i in range(1, len(self.daily_data)):
                # format fields from row based on content
                # is status cell matches pattern_inprogress, highlight text
                if self.pattern_inprogress.match(self.daily_data[f'row_{i}'][3]):
                    task_num = "[bright_white]" + self.daily_data[f'row_{i}'][0]
                    description = "[bright_white]" + self.daily_data[f'row_{i}'][1]
                elif self.pattern_closed.match(self.daily_data[f'row_{i}'][3]):
                    task_num = "[dim]" + self.daily_data[f'row_{i}'][0]
                    description = "[dim]" + self.daily_data[f'row_{i}'][1]
                # if status cell matches pattern_open or no pattern, no changes to format
                else:
                    task_num = self.daily_data[f'row_{i}'][0]
                    description = self.daily_data[f'row_{i}'][1]

                # format prio cell
                # if prio == 1, then red number (prio in column index 2)
                if self.daily_data[f'row_{i}'][2] == '1':
                    prio = '[red]1'
                elif self.daily_data[f'row_{i}'][2] == '1' and self.pattern_inprogress.match(
                        self.daily_data[f'row_{i}'][3]):
                    prio = "[bright_red]1"
                else:
                    prio = self.daily_data[f'row_{i}'][2]

                table.add_row(
                    task_num,
                    description,
                    prio,
                    self.convert_status_code(self.daily_data[f'row_{i}'][3]),
                )
        else:
            table.add_row(None, '[purple]No task available', None, None)

        self.layout['left_lower'].update(Align(table, align='center', vertical='top'))

    def render_table_general(self):
        table = Table(box=box.SQUARE,
                      leading=True, highlight=False,
                      header_style='black on white',
                      style='black')
        for column in self.general_data['row_0']:
            table.add_column(column, justify='center')
        # check that the table contains rows below the header row
        if len(self.general_data) > 1:
            for i in range(1, len(self.general_data)):
                # format fields from row based on content
                # is status cell matches pattern_inprogress, highlight text
                if self.pattern_inprogress.match(self.general_data[f'row_{i}'][3]):
                    task_num = "[bright_white]" + self.general_data[f'row_{i}'][0]
                    description = "[bright_white]" + self.general_data[f'row_{i}'][1]
                elif self.pattern_closed.match(self.general_data[f'row_{i}'][3]):
                    task_num = "[dim]" + self.general_data[f'row_{i}'][0]
                    description = "[dim]" + self.general_data[f'row_{i}'][1]
                # if status cell matches pattern_open or no pattern, no changes to format
                else:
                    task_num = self.general_data[f'row_{i}'][0]
                    description = self.general_data[f'row_{i}'][1]

                # format prio cell
                # if prio == 1, then red number (prio in column index 2)
                if self.general_data[f'row_{i}'][2] == '1':
                    prio = '[red]1'
                elif self.general_data[f'row_{i}'][2] == '1' and self.pattern_inprogress.match(
                        self.general_data[f'row_{i}'][3]):
                    prio = "[bright_red]1"
                else:
                    prio = self.general_data[f'row_{i}'][2]

                table.add_row(
                    task_num,
                    description,
                    prio,
                    self.convert_status_code(self.general_data[f'row_{i}'][3]),
                )
        else:
            table.add_row(None, '[purple]No task available', None, None)

        self.layout['right_lower'].update(Align(table, align='center'))

    def render_notes(self):
        """
        Updates the table in the layout object based on the notes_data attribute.

        Use get_notes() to update the data before updating the table.
        """
        table = Table(box=box.SQUARE,
                      highlight=False,
                      show_header=False,
                      border_style='black',
                      )
        table.add_column('notes', justify='center')  # omitted
        if len(self.notes_data) > 0 and self.notes_data[f'row_0'][0] != '':
            for i in range(0, len(self.notes_data)):
                table.add_row(self.notes_data[f'row_{i}'][0])
                # do not print a divider after the last row
                if i == len(self.notes_data) - 1:
                    break
                table.add_row('[dim]──' * 10)

        self.layout['content_bottom_notes'].update(Align(table, align='center'))

    def render_footer(self, _time: float):
        self.layout['bottom_left'].update(
            Align(
                Panel(f'Uptime: {datetime.now().replace(microsecond=0) - self.boot_time}',
                      box=box.SQUARE),
                align='center'))
        self.layout['bottom_mid'].update(
            Align(
                Panel(
                    f'Updated at [bright_cyan]{datetime.now().strftime("%H:%M:%S")}[/bright_cyan] in [cyan]{_time:.2f}[/cyan]s',
                    box=box.SQUARE),
                align='center'))
        self.layout['bottom_right'].update(
            Align(
                Panel(f'v{__VERSION__}', box=box.SQUARE, style='bright_black'), align='center'))

    def get_data(self, _type=None):
        """
        Refreshes the data data from Notion API into the dashboard object and
        returns the update time.

        Refreshes the daily or general task table data and
        corresponding dashboard element depending on the argument provided.
        """
        time_start = time.time()
        if _type == 'daily':
            # UPDATE WITH YOUR OWN URL
            url = "https://api.notion.com/v1/blocks/XXX/children?page_size=100"
        elif _type == 'general':
            # UPDATE WITH YOUR OWN URL
            url = "https://api.notion.com/v1/blocks/XXX/children?page_size=100"
        else:
            print('"type" argument has to be one of ["daily", "general"]')
            sys.exit(1)

        # UPDATE WITH YOUR OWN API ACCESS TOKEN
        headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-02-22",
            "Authorization": "XXX"
        }

        response = requests.request("GET", url, headers=headers)

        _json = json.loads(response.text)
        table_rows = _json['results']
        table_content = {}
        for i in range(0, len(table_rows), 1):
            row = table_rows[i]['table_row']['cells']
            table_content[f'row_{i}'] = []
            for cell in row:
                table_content[f'row_{i}'].append(cell[0]['plain_text'])
        if _type == 'daily':
            self.daily_data = table_content
        elif _type == 'general':
            self.general_data = table_content
        time_end = time.time()
        return time_end - time_start

    def get_notes(self):
        """
        Refreshes the notes data from Notion API in the dashboard object and
        returns the update time
        """
        time_start = time.time()

        # UPDATE WITH YOUR OWN URL
        url = "https://api.notion.com/v1/blocks/XXX/children?page_size=100"

        # UPDATE WITH YOUR OWN API ACCESS TOKEN AS ABOVE
        headers = {
            "Accept": "application/json",
            "Notion-Version": "2022-02-22",
            "Authorization": "XXX"
        }

        response = requests.request("GET", url, headers=headers)

        _json = json.loads(response.text)
        table_rows = _json['results']
        table_content = {}
        for i in range(0, len(table_rows), 1):
            row = table_rows[i]['table_row']['cells']
            table_content[f'row_{i}'] = []
            # check for empty table
            if len(row[0]) == 0:
                table_content[f'row_{i}'].append('[bright_black]Nothing here to see')
                break
            for cell in row:
                table_content[f'row_{i}'].append(cell[0]['plain_text'])
        self.notes_data = table_content
        time_end = time.time()
        return time_end - time_start

    def get_score(self):
        # total score
        opened = 0
        closed = 0
        # get daily
        for i in range(1, len(self.daily_data), 1):
            if bool(self.pattern_closed.match(self.daily_data[f'row_{i}'][3])):
                closed += 1
            else:
                opened += 1
        # get general
        for i in range(1, len(self.general_data), 1):
            if bool(self.pattern_closed.match(self.general_data[f'row_{i}'][3])):
                closed += 1
            else:
                opened += 1
        n_total = opened + closed
        if closed == n_total:
            self.score_total = '[bright_green]                ALL DONE                '
        else:
            self.score_total = str(gen_progress_bar(closed, n_total))

        # prio score
        opened = 0
        closed = 0
        # get daily prio 1's
        for i in range(1, len(self.daily_data), 1):
            if self.daily_data[f'row_{i}'][2] == '1':
                if bool(self.pattern_closed.match(self.daily_data[f'row_{i}'][3])):
                    closed += 1
                else:
                    opened += 1
        # get general prio 1's
        for i in range(1, len(self.general_data), 1):
            if self.general_data[f'row_{i}'][2] == '1':
                if bool(self.pattern_closed.match(self.general_data[f'row_{i}'][3])):
                    closed += 1
                else:
                    opened += 1

        if opened == 0:
            self.score_prio = 'PRIO [bright_green]ALL DONE'
        else:
            self.score_prio = str(gen_progress_bar(closed, opened + closed, length=10, prefix='PRIO'))

    def convert_status_code(self, status_field):
        """
        Converts Notion status codes (Status column field) to full code + color if matched with pattern.
        If no pattern is matched, code sill be output dimmed.

        :return:
        Full colored status code according to matched pattern.
        """
        if self.pattern_open.match(status_field):
            return "[yellow]open"
        elif self.pattern_inprogress.match(status_field):
            return "[magenta]in progress"
        elif self.pattern_closed.match(status_field):
            return "[green]closed"
        else:
            return "[dim]" + status_field


def gen_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█'):
    # https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'\r{prefix} |{bar}| {percent}% {suffix}'


def re_patterns():
    """
    Compiles and returns regex patterns for matching of status codes
    """
    pattern_open = re.compile(r"[o|O]p?e?n?\Z")
    pattern_inprogress = re.compile(r"[i|I]n?\s?[p|P]r?o?g?r?e?s?s?\Z")
    pattern_closed = re.compile(r"[c|C]l?o?s?e?d?\Z")
    return pattern_open, pattern_inprogress, pattern_closed


def connection_error():
    console.clear()
    console.rule('[red]ERROR')
    console.print("ConnectionError: Failed to establish a new connection.")
    console.rule()
    console.print('retry in 30s')
    time.sleep(30)
    sys.exit()


def usr_interrupt():
    console.clear()
    _input = Prompt.ask('Refresh or exit?', console=console, choices=['r', 'e'], default='r')
    if _input == 'e':
        sys.exit(0)
    else:
        return _input
