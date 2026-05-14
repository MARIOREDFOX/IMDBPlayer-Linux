#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import subprocess
import re
import webbrowser

# Built-in movie database
MOVIE_DATABASE = {
    'avatar': {'title': 'Avatar', 'imdb_id': 'tt0499549', 'year': '2009'},
    'avatar 2': {'title': 'Avatar: The Way of Water', 'imdb_id': 'tt1630029', 'year': '2022'},
    'inception': {'title': 'Inception', 'imdb_id': 'tt1375666', 'year': '2010'},
    'titanic': {'title': 'Titanic', 'imdb_id': 'tt0120338', 'year': '1997'},
    'dark knight': {'title': 'The Dark Knight', 'imdb_id': 'tt0468569', 'year': '2008'},
    'interstellar': {'title': 'Interstellar', 'imdb_id': 'tt0816692', 'year': '2014'},
    'gladiator': {'title': 'Gladiator', 'imdb_id': 'tt0172495', 'year': '2000'},
    'matrix': {'title': 'The Matrix', 'imdb_id': 'tt0133093', 'year': '1999'},
    'automata': {'title': 'Autómata', 'imdb_id': 'tt1971325', 'year': '2014'},
    'pulp fiction': {'title': 'Pulp Fiction', 'imdb_id': 'tt0110912', 'year': '1994'},
    'fight club': {'title': 'Fight Club', 'imdb_id': 'tt0137523', 'year': '1999'},
    'shawshank': {'title': 'The Shawshank Redemption', 'imdb_id': 'tt0111161', 'year': '1994'},
    'godfather': {'title': 'The Godfather', 'imdb_id': 'tt0068646', 'year': '1972'},
    'terminator': {'title': 'The Terminator', 'imdb_id': 'tt0088247', 'year': '1984'},
    'jurassic park': {'title': 'Jurassic Park', 'imdb_id': 'tt0107290', 'year': '1993'},
    'forrest gump': {'title': 'Forrest Gump', 'imdb_id': 'tt0109830', 'year': '1994'},
}

class IMDBPlayerApp:
    def __init__(self):
        # Create main window
        self.window = Gtk.Window(title="IMDB Movie Player")
        self.window.set_default_size(800, 650)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        # Apply styling
        self.apply_style()
        
        # Create header bar
        self.create_header_bar()
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.add(main_box)
        
        # Scrolled content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scrolled, True, True, 0)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content.set_margin_top(30)
        content.set_margin_bottom(30)
        content.set_margin_start(40)
        content.set_margin_end(40)
        scrolled.add(content)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<span size='x-large' weight='bold'>🎬 IMDB Movie Player</span>")
        title.set_halign(Gtk.Align.CENTER)
        content.pack_start(title, False, False, 0)
        
        subtitle = Gtk.Label()
        subtitle.set_markup("<span foreground='#888888'>Opens movies in your web browser</span>")
        subtitle.set_halign(Gtk.Align.CENTER)
        content.pack_start(subtitle, False, False, 0)
        
        # Search section
        search_frame = self.create_frame("🔍 Search by Movie Name")
        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        search_box.set_margin_top(15)
        search_box.set_margin_bottom(15)
        search_box.set_margin_start(15)
        search_box.set_margin_end(15)
        
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Enter movie name (e.g., Avatar, Inception)")
        self.search_entry.set_size_request(500, 45)
        self.search_entry.connect("activate", self.on_search)
        search_box.pack_start(self.search_entry, False, False, 0)
        
        search_btn = Gtk.Button.new_with_label("🔍 Search")
        search_btn.set_size_request(150, 40)
        search_btn.connect("clicked", self.on_search)
        search_btn.get_style_context().add_class("suggested-action")
        search_box.pack_start(search_btn, False, False, 0)
        
        search_frame.add(search_box)
        content.pack_start(search_frame, False, False, 0)
        
        # OR divider
        or_label = Gtk.Label()
        or_label.set_markup("<span foreground='#555555'>──────  OR  ──────</span>")
        or_label.set_halign(Gtk.Align.CENTER)
        content.pack_start(or_label, False, False, 0)
        
        # URL section
        url_frame = self.create_frame("📋 Paste IMDB URL")
        url_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        url_box.set_margin_top(15)
        url_box.set_margin_bottom(15)
        url_box.set_margin_start(15)
        url_box.set_margin_end(15)
        
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("https://www.imdb.com/title/tt0499549/")
        self.url_entry.set_size_request(500, 45)
        self.url_entry.connect("activate", self.play_url)
        url_box.pack_start(self.url_entry, False, False, 0)
        
        play_btn = Gtk.Button.new_with_label("🌐 Open in Browser")
        play_btn.set_size_request(150, 40)
        play_btn.connect("clicked", self.play_url)
        play_btn.get_style_context().add_class("suggested-action")
        url_box.pack_start(play_btn, False, False, 0)
        
        url_frame.add(url_box)
        content.pack_start(url_frame, False, False, 0)
        
        # Popular movies
        popular_label = Gtk.Label()
        popular_label.set_markup("<b>⭐ Popular Movies (Click to play)</b>")
        popular_label.set_halign(Gtk.Align.START)
        content.pack_start(popular_label, False, False, 0)
        
        popular_grid = Gtk.Grid()
        popular_grid.set_row_spacing(8)
        popular_grid.set_column_spacing(8)
        popular_grid.set_halign(Gtk.Align.FILL)
        
        popular_movies = [
            "Avatar", "Inception", "Titanic", "Gladiator",
            "The Matrix", "Interstellar", "Pulp Fiction", 
            "Autómata", "Fight Club", "The Godfather"
        ]
        
        row, col = 0, 0
        for movie in popular_movies:
            btn = Gtk.Button.new_with_label(movie)
            btn.set_size_request(120, 40)
            btn.connect("clicked", self.on_popular, movie)
            popular_grid.attach(btn, col, row, 1, 1)
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        content.pack_start(popular_grid, False, False, 0)
        
        # Results section
        self.results_label = Gtk.Label()
        self.results_label.set_markup("<b>📋 Search Results:</b>")
        self.results_label.set_halign(Gtk.Align.START)
        self.results_label.set_margin_top(20)
        content.pack_start(self.results_label, False, False, 0)
        
        self.results_list = Gtk.ListBox()
        self.results_list.set_selection_mode(Gtk.SelectionMode.NONE)
        content.pack_start(self.results_list, False, False, 0)
        
        # Info bar
        info_bar = Gtk.InfoBar()
        info_bar.set_message_type(Gtk.MessageType.INFO)
        info_box = info_bar.get_content_area()
        info_label = Gtk.Label()
        info_label.set_markup("💡 Videos will open in your default web browser (Chrome/Firefox)")
        info_box.pack_start(info_label, False, False, 0)
        content.pack_start(info_bar, False, False, 0)
        
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
    
    def apply_style(self):
        css = b"""
            window {
                background-color: #1e1e1e;
            }
            GtkFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
                border: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.5);
            }
            GtkLabel {
                color: #ffffff;
            }
            GtkEntry {
                background-color: #3d3d3d;
                color: #ffffff;
                border-radius: 8px;
                border: 1px solid #555555;
                padding: 8px;
            }
            GtkEntry:focus {
                border: 1px solid #0078D7;
            }
            GtkButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border-radius: 8px;
                padding: 8px 16px;
            }
            GtkButton:hover {
                background-color: #4d4d4d;
            }
            .suggested-action {
                background-color: #0078D7;
            }
            .suggested-action:hover {
                background-color: #1060a0;
            }
            GtkListBoxRow {
                background-color: #2d2d2d;
                border-radius: 8px;
                margin: 5px;
            }
            GtkListBoxRow:hover {
                background-color: #3d3d3d;
            }
            GtkInfoBar {
                background-color: #2d2d2d;
                border-radius: 8px;
            }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_frame(self, title):
        frame = Gtk.Frame()
        label = Gtk.Label()
        label.set_markup(f"<b>{title}</b>")
        label.set_halign(Gtk.Align.CENTER)
        frame.set_label_widget(label)
        return frame
    
    def create_header_bar(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title("IMDB Movie Player")
        header.set_subtitle("Opens in Browser")
        
        about_btn = Gtk.Button.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        about_btn.connect("clicked", self.show_about)
        header.pack_end(about_btn)
        
        self.window.set_titlebar(header)
    
    def on_search(self, widget):
        query = self.search_entry.get_text().strip().lower()
        if not query:
            self.show_error("Please enter a movie name")
            return
        
        # Clear results
        for child in self.results_list.get_children():
            self.results_list.remove(child)
        
        # Search
        results = []
        for key, movie in MOVIE_DATABASE.items():
            if query in key or key in query:
                results.append(movie)
        
        if not results:
            self.show_error(f"No results found for '{query}'")
            return
        
        # Display results
        for movie in results:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
            hbox.set_margin_top(12)
            hbox.set_margin_bottom(12)
            hbox.set_margin_start(15)
            hbox.set_margin_end(15)
            
            info = Gtk.Label()
            info.set_markup(f"<b>{movie['title']}</b>  ({movie['year']})  -  {movie['imdb_id']}")
            info.set_halign(Gtk.Align.START)
            info.set_hexpand(True)
            hbox.pack_start(info, True, True, 0)
            
            play = Gtk.Button.new_with_label("▶ Watch")
            play.set_size_request(100, 35)
            play.get_style_context().add_class("suggested-action")
            play.connect("clicked", self.play_movie, movie)
            hbox.pack_start(play, False, False, 0)
            
            row.add(hbox)
            self.results_list.add(row)
        
        self.results_list.show_all()
        self.results_label.set_markup(f"<b>📋 Search Results ({len(results)} found):</b>")
    
    def on_popular(self, button, movie_name):
        # Find movie in database
        for key, movie in MOVIE_DATABASE.items():
            if key == movie_name.lower() or movie['title'].lower() == movie_name.lower():
                self.play_movie(None, movie)
                return
    
    def play_url(self, widget):
        url = self.url_entry.get_text().strip()
        if not url:
            self.show_error("Please enter a URL")
            return
        
        imdb_match = re.search(r'tt\d+', url)
        if imdb_match:
            play_url = f"https://www.playimdb.com/title/{imdb_match.group(0)}/"
            self.open_in_browser(play_url)
        else:
            self.show_error("Invalid IMDB URL.\n\nExample: https://www.imdb.com/title/tt0499549/")
    
    def play_movie(self, button, movie):
        play_url = f"https://www.playimdb.com/title/{movie['imdb_id']}/"
        self.open_in_browser(play_url)
    
    def open_in_browser(self, url):
        """Open the URL in default web browser"""
        webbrowser.open(url)
        
        # Show confirmation dialog
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="🎬 Opening in Browser"
        )
        dialog.format_secondary_text(
            "The movie will open in your default web browser.\n\n"
            "Once the page loads, click the play button on the video player."
        )
        dialog.run()
        dialog.destroy()
    
    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def show_about(self, button):
        dialog = Gtk.AboutDialog()
        dialog.set_transient_for(self.window)
        dialog.set_program_name("IMDB Movie Player")
        dialog.set_version("1.0.0")
        dialog.set_comments("Watch movies from IMDB using playimdb.com")
        dialog.set_copyright("© 2024")
        dialog.set_license_type(Gtk.License.MIT)
        dialog.set_authors(["Mario"])
        dialog.run()
        dialog.destroy()

def main():
    Gtk.init(None)
    app = IMDBPlayerApp()
    Gtk.main()

if __name__ == "__main__":
    main()
