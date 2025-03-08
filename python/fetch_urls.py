import urllib.request
import re
import json
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Webhook URL (Replace with your actual webhook)
WEBHOOK_URL = "https://your-webhook-url.com"
PAYLOAD_FILE = "submitted_payload.txt"  # Prevents duplicate submissions

def fetch_page(url):
    """Fetch the page source using urllib (built-in)."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch page: {e}")
        return None

def extract_urls(html):
    """Extract all URLs from page source."""
    urls = list(set(re.findall(r"https?://[^\s\"'>]+", html)))  # Finds all URLs
    return urls

def extract_payload(html):
    """Extract JSON payload from the page source."""
    match = re.search(r'payload\s*=\s*(\{.*?\})', html, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Could not parse JSON payload.")
    return None

def send_to_webhook(payload):
    """Send extracted payload to the webhook (only once)."""
    if os.path.exists(PAYLOAD_FILE):
        messagebox.showinfo("Info", "Payload already sent. Aborting.")
        return

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                with open(PAYLOAD_FILE, "w") as file:
                    file.write(json.dumps(payload))  # Store sent payload
                messagebox.showinfo("Success", "Successfully sent payload to webhook.")
            else:
                messagebox.showerror("Error", f"Webhook response error: {response.status}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send payload: {e}")

def process_url():
    """Handles the fetching, extracting, and displaying of data."""
    url = url_entry.get().strip()
    if not url.startswith("http"):
        messagebox.showerror("Error", "Please enter a valid URL (starting with http or https).")
        return

    log_output.config(state=tk.NORMAL)
    log_output.delete(1.0, tk.END)  # Clear previous results
    log_output.insert(tk.END, "🔄 Fetching page content...\n")
    log_output.config(state=tk.DISABLED)
    root.update()

    html = fetch_page(url)
    if not html:
        return

    log_output.config(state=tk.NORMAL)
    log_output.insert(tk.END, "🔍 Extracting URLs...\n")
    log_output.config(state=tk.DISABLED)
    root.update()

    urls = extract_urls(html)
    log_output.config(state=tk.NORMAL)
    log_output.insert(tk.END, "\n".join(urls) if urls else "⚠️ No URLs found.\n")
    log_output.insert(tk.END, "\n\n")
    log_output.config(state=tk.DISABLED)

    payload = extract_payload(html)
    if payload:
        log_output.config(state=tk.NORMAL)
        log_output.insert(tk.END, "✅ Payload Extracted!\n")
        log_output.insert(tk.END, json.dumps(payload, indent=2) + "\n\n")
        log_output.config(state=tk.DISABLED)

        send_to_webhook(payload)
    else:
        log_output.config(state=tk.NORMAL)
        log_output.insert(tk.END, "⚠️ No payload found on the page.\n")
        log_output.config(state=tk.DISABLED)

    root.update()

# GUI Setup
root = tk.Tk()
root.title("Web Page URL Extractor")
root.geometry("600x500")

tk.Label(root, text="Enter Website URL:").pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Extract URLs", command=process_url)
fetch_button.pack(pady=5)

log_output = scrolledtext.ScrolledText(root, width=70, height=20, state=tk.DISABLED)
log_output.pack(pady=10)

root.mainloop()
