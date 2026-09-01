import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from main import process_quotes


class QuoteCalculatorApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Bulk Quote Calculator")
        self.geometry("700x450")
        self.resizable(False, False)

        self.input_file = tk.StringVar()
        self.display_file = tk.StringVar(value="No file selected")
        self.status_text = tk.StringVar(value="Ready")
        self.output_file = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Bulk Quote Calculator",
            font=("Segoe UI", 20, "bold")
        )
        title_label.pack(pady=(0, 8))

        subtitle_label = ttk.Label(
            main_frame,
            text="Import an Excel workbook and generate validated quote results."
        )
        subtitle_label.pack(pady=(0, 25))

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill="x", pady=10)

        file_entry = ttk.Entry(
            file_frame,
            textvariable=self.display_file,
            state="readonly"
        )
        file_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        browse_button = ttk.Button(
            file_frame,
            text="Select Excel File",
            command=self.browse_file
        )
        browse_button.pack(side="right")

        self.calculate_button = ttk.Button(
            main_frame,
            text="Calculate Quotes",
            command=self.calculate_quotes
        )
        self.calculate_button.pack(
            fill="x",
            pady=(20, 10)
        )

        self.open_button = tk.Button(
            main_frame,
            text="Open Results",
            command=self.open_results,
            state="disabled"
        )
        self.open_button.pack(fill="x")

        separator = ttk.Separator(
            main_frame,
            orient="horizontal"
        )
        separator.pack(fill="x", pady=(20, 12))

        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text
        )
        status_label.pack()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Quote Workbook",
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if filename:
            self.input_file.set(filename)
            self.display_file.set(Path(filename).name)
            self.status_text.set("File selected. Ready to calculate.")
            self.open_button.config(state="disabled")
            self.output_file = None

    def calculate_quotes(self):
        input_filename = self.input_file.get()

        if not input_filename:
            messagebox.showwarning(
                "No File Selected",
                "Please select an Excel workbook first."
            )
            return

        input_path = Path(input_filename)

        self.output_file = input_path.with_name(
            "quote_results.xlsx"
        )

        self.calculate_button.config(state="disabled")
        self.status_text.set("Processing workbook...")
        self.update_idletasks()

        try:
            summary = process_quotes(
                input_filename,
                str(self.output_file)
            )

            successful = summary["successful"]
            errors = summary["errors"]

            success_word = "quote" if successful == 1 else "quotes"
            error_word = "row" if errors == 1 else "rows"

            self.status_text.set(
                f"{successful} {success_word} calculated | "
                f"{errors} {error_word} with errors"
            )

            self.open_button.config(state="normal")

            messagebox.showinfo(
                "Calculation Complete",
                f"{successful} {success_word} calculated successfully.\n"
                f"{errors} {error_word} contained validation errors."
            )

        except Exception as error:
            self.status_text.set("Processing failed.")

            messagebox.showerror(
                "Processing Error",
                f"Unable to process workbook:\n\n{error}"
            )

        finally:
            self.calculate_button.config(state="normal")

    def open_results(self):
        if not self.output_file or not self.output_file.exists():
            messagebox.showerror(
                "File Not Found",
                "The results workbook could not be found."
            )
            return

        os.startfile(self.output_file)


if __name__ == "__main__":
    app = QuoteCalculatorApp()
    app.mainloop()