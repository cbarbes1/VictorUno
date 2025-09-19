"""GUI interface for VictorUno using tkinter."""

import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import sys
from pathlib import Path
from typing import Optional

from ..core.agent import VictorUnoAgent
from ..core.config import Config


class VictorUnoGUI:
    """GUI interface for VictorUno."""
    
    def __init__(self):
        """Initialize the GUI."""
        self.config = Config.from_env()
        self.agent = VictorUnoAgent(self.config)
        self.thread_id = "gui_session"
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"{self.config.agent_name} - Personal AI Assistant")
        self.root.geometry(f"{self.config.gui_width}x{self.config.gui_height}")
        
        # Configure theme
        self.setup_theme()
        
        # Create UI elements
        self.create_widgets()
        
        # Set up event loop for async operations
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
    
    def setup_theme(self):
        """Set up the GUI theme."""
        style = ttk.Style()
        
        if self.config.gui_theme == "dark":
            # Dark theme colors
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            select_bg = "#404040"
            
            self.root.configure(bg=bg_color)
            
            style.theme_use("clam")
            style.configure("TFrame", background=bg_color)
            style.configure("TLabel", background=bg_color, foreground=fg_color)
            style.configure("TButton", background="#404040", foreground=fg_color)
            style.configure("TEntry", background="#404040", foreground=fg_color)
            style.map("TButton", background=[("active", "#505050")])
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text=f"🤖 {self.config.agent_name}",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Personal AI Assistant for Research, Development, and Optimization",
            font=("Arial", 10)
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Chat area
        chat_frame = ttk.Frame(main_frame)
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Consolas", 10),
            bg="#1e1e1e" if self.config.gui_theme == "dark" else "#ffffff",
            fg="#ffffff" if self.config.gui_theme == "dark" else "#000000",
            insertbackground="#ffffff" if self.config.gui_theme == "dark" else "#000000"
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(
            input_frame,
            textvariable=self.message_var,
            font=("Arial", 10)
        )
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send button
        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
        send_button.grid(row=0, column=1, padx=(5, 0))
        
        # Control buttons frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Upload button
        upload_button = ttk.Button(
            controls_frame,
            text="📎 Upload Document",
            command=self.upload_document
        )
        upload_button.grid(row=0, column=0, padx=(0, 5))
        
        # Clear button
        clear_button = ttk.Button(
            controls_frame,
            text="🔄 Clear Chat",
            command=self.clear_chat
        )
        clear_button.grid(row=0, column=1, padx=(5, 0))
        
        # Settings button
        settings_button = ttk.Button(
            controls_frame,
            text="⚙️ Settings",
            command=self.open_settings
        )
        settings_button.grid(row=0, column=2, padx=(5, 0))
        
        # Chrome integration button
        chrome_button = ttk.Button(
            controls_frame,
            text="🌐 Web Research",
            command=self.start_web_research
        )
        chrome_button.grid(row=0, column=3, padx=(5, 0))
        
        # Initial message
        self.add_message("VictorUno", "Hello! I'm your personal AI assistant. How can I help you today?", "ai")
        
        # Focus on input
        self.message_entry.focus()
    
    def _run_event_loop(self):
        """Run the asyncio event loop in a separate thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    def add_message(self, sender: str, message: str, msg_type: str = "user"):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding
        if msg_type == "ai":
            color = "#00aaff" if self.config.gui_theme == "dark" else "#0066cc"
            sender_text = f"[{timestamp}] 🤖 {sender}: "
        elif msg_type == "system":
            color = "#ffaa00" if self.config.gui_theme == "dark" else "#ff6600"
            sender_text = f"[{timestamp}] ⚙️ {sender}: "
        else:
            color = "#00ff00" if self.config.gui_theme == "dark" else "#006600"
            sender_text = f"[{timestamp}] 🧑 {sender}: "
        
        # Insert sender
        start_pos = self.chat_display.index(tk.INSERT)
        self.chat_display.insert(tk.END, sender_text)
        end_pos = self.chat_display.index(tk.INSERT)
        self.chat_display.tag_add(f"sender_{msg_type}", start_pos, end_pos)
        self.chat_display.tag_config(f"sender_{msg_type}", foreground=color, font=("Arial", 10, "bold"))
        
        # Insert message
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self, event=None):
        """Send a message to the agent."""
        message = self.message_var.get().strip()
        if not message:
            return
        
        # Add user message to display
        self.add_message("You", message, "user")
        
        # Clear input
        self.message_var.set("")
        
        # Send to agent asynchronously
        future = asyncio.run_coroutine_threadsafe(
            self._send_message_async(message),
            self.loop
        )
        
        # Schedule result handling
        self.root.after(100, lambda: self._check_future(future))
    
    async def _send_message_async(self, message: str):
        """Send message to agent asynchronously."""
        try:
            response = await self.agent.chat(message, self.thread_id)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _check_future(self, future):
        """Check if the async operation is complete."""
        if future.done():
            try:
                response = future.result()
                self.add_message("VictorUno", response, "ai")
            except Exception as e:
                self.add_message("System", f"Error: {str(e)}", "system")
        else:
            # Check again in 100ms
            self.root.after(100, lambda: self._check_future(future))
    
    def upload_document(self):
        """Upload and process a document."""
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Text files", "*.txt"),
                ("Word documents", "*.docx"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.add_message("System", f"Uploading document: {Path(file_path).name}", "system")
            
            # Process document asynchronously
            future = asyncio.run_coroutine_threadsafe(
                self.agent.process_document(Path(file_path)),
                self.loop
            )
            
            # Schedule result handling
            self.root.after(100, lambda: self._check_upload_future(future))
    
    def _check_upload_future(self, future):
        """Check if the document upload is complete."""
        if future.done():
            try:
                result = future.result()
                self.add_message("System", result, "system")
            except Exception as e:
                self.add_message("System", f"Upload error: {str(e)}", "system")
        else:
            # Check again in 100ms
            self.root.after(100, lambda: self._check_upload_future(future))
    
    def clear_chat(self):
        """Clear the chat history."""
        response = messagebox.askyesno(
            "Clear Chat",
            "Are you sure you want to clear the chat history?"
        )
        
        if response:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            # Reset agent conversation
            self.agent.reset_conversation(self.thread_id)
            
            # Add welcome message
            self.add_message("VictorUno", "Chat cleared. How can I help you?", "ai")
    
    def open_settings(self):
        """Open settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#2b2b2b" if self.config.gui_theme == "dark" else "#ffffff")
        
        # Settings content
        ttk.Label(settings_window, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(settings_window, text="Settings panel coming soon...").pack(pady=20)
        
        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=10)
    
    def start_web_research(self):
        """Start web research functionality."""
        query = tk.simpledialog.askstring(
            "Web Research",
            "Enter your research query:",
            parent=self.root
        )
        
        if query:
            self.add_message("System", f"Starting web research for: {query}", "system")
            
            # Perform web research asynchronously
            future = asyncio.run_coroutine_threadsafe(
                self.agent.web_search(query),
                self.loop
            )
            
            # Schedule result handling
            self.root.after(100, lambda: self._check_research_future(future))
    
    def _check_research_future(self, future):
        """Check if the web research is complete."""
        if future.done():
            try:
                result = future.result()
                self.add_message("System", result, "system")
            except Exception as e:
                self.add_message("System", f"Research error: {str(e)}", "system")
        else:
            # Check again in 100ms
            self.root.after(100, lambda: self._check_research_future(future))
    
    def run(self):
        """Start the GUI."""
        try:
            self.root.mainloop()
        finally:
            # Clean up
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.thread.join(timeout=1)


def run_gui():
    """Run the GUI interface."""
    try:
        import tkinter.simpledialog
        globals()['tkinter.simpledialog'] = tkinter.simpledialog
        
        gui = VictorUnoGUI()
        gui.run()
    except ImportError as e:
        print(f"GUI dependencies not available: {e}")
        print("Install GUI dependencies with: pip install victoruno[gui]")
        sys.exit(1)


if __name__ == "__main__":
    run_gui()