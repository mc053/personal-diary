from markupsafe import Markup

class DiaryEntry:
    def __init__(self, date, content):
        self.date = date
        self.content = content

    def display_in_html(self, markup):
        return Markup(markup)

class TextEntry(DiaryEntry):
    def display_in_html(self):
        return super().display_in_html('''
        <div class="text_entry">
            <p>%s</p>
        </div>
        ''' %self.content)

class PictureEntry(DiaryEntry):
    def display_in_html(self):
        return super().display_in_html('''
        <div class="picture_entry">
            <img src=%s width="500"/>
        </div>
        ''' %self.content)
