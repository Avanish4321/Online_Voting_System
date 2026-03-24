import tkinter as tk
from tkinter import messagebox
import json
import os

def load_data(file):
    if not os.path.exists(file):
        messagebox.showerror("Error", f"Missing file: {file}")
        return {}
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def admin_login(action_callback):
    def verify():
        if password_entry.get() == "admin@1234":  # ✅ Updated password
            login_win.destroy()
            action_callback()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    login_win = tk.Toplevel(root)
    login_win.title("Admin Login")
    login_win.configure(bg="#FFEFD5")
    login_win.geometry("250x120")

    tk.Label(login_win, text="Enter Admin Password:", bg="#FFEFD5", font=("Helvetica", 10)).pack(pady=10)
    password_entry = tk.Entry(login_win, show="*", font=("Helvetica", 10))
    password_entry.pack()
    tk.Button(login_win, text="Submit", command=verify, bg="#8B0000", fg="white").pack(pady=10)

def cast_vote(voter_id, candidate):
    voters = load_data('voters.json')
    candidates = load_data('candidates.json')

    if not voters or not candidates:
        return

    if voter_id not in voters['voters']:
        messagebox.showerror("Error", "Invalid Voter ID.")
        return

    if voters['voters'][voter_id]:
        messagebox.showwarning("Warning", "You have already voted.")
        return

    candidates['candidates'][candidate] += 1
    voters['voters'][voter_id] = True
    save_data('candidates.json', candidates)
    save_data('voters.json', voters)
    messagebox.showinfo("Success", "Your vote has been cast!")

def show_results():
    candidates = load_data('candidates.json')
    if not candidates:
        return
    sorted_candidates = sorted(candidates['candidates'].items(), key=lambda x: x[1], reverse=True)
    result_text = "\n".join([f"{name}: {votes} votes" for name, votes in sorted_candidates])
    winner = sorted_candidates[0][0]
    result_text += f"\n\n🏆 Leading Candidate: {winner}"
    messagebox.showinfo("Voting Results", result_text)

def reset_votes():
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all votes?"):
        voters = load_data('voters.json')
        candidates = load_data('candidates.json')
        if not voters or not candidates:
            return
        for voter in voters['voters']:
            voters['voters'][voter] = False
        for candidate in candidates['candidates']:
            candidates['candidates'][candidate] = 0
        save_data('voters.json', voters)
        save_data('candidates.json', candidates)
        messagebox.showinfo("Reset Complete", "All votes and voter statuses have been reset.")

def vote_window():
    voter_id = voter_id_entry.get().strip()
    if not voter_id:
        messagebox.showerror("Error", "Please enter your Voter ID.")
        return
    if not voter_id.isalnum():
        messagebox.showerror("Error", "Voter ID must be alphanumeric.")
        return

    vote_win = tk.Toplevel(root)
    vote_win.title("Cast Your Vote")
    vote_win.configure(bg="#FFF8DC")

    tk.Label(vote_win, text="Choose your candidate:", font=("Helvetica", 12, "bold"), bg="#FFF8DC").pack(pady=10)

    selected = tk.StringVar()
    candidates = load_data('candidates.json')
    if not candidates:
        vote_win.destroy()
        return

    for name in candidates['candidates']:
        tk.Radiobutton(vote_win, text=name, variable=selected, value=name,
                       font=("Helvetica", 11), bg="#FFF8DC", anchor='w').pack(fill='x', padx=20)

    def submit():
        if selected.get():
            cast_vote(voter_id, selected.get())
            vote_win.destroy()
        else:
            messagebox.showerror("Error", "Please select a candidate.")

    tk.Button(vote_win, text="Submit Vote", command=submit, bg="#228B22", fg="white",
              font=("Helvetica", 11, "bold")).pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("🇮🇳 Indian Voting System")
root.geometry("360x360")
root.configure(bg="#F0E68C")

tk.Label(root, text="Enter your Voter ID:", font=("Helvetica", 12), bg="#F0E68C").pack(pady=10)
voter_id_entry = tk.Entry(root, font=("Helvetica", 11))
voter_id_entry.pack()

tk.Button(root, text="Vote", command=vote_window, bg="#1E90FF", fg="white",
          font=("Helvetica", 11, "bold")).pack(pady=10)

tk.Button(root, text="View Results (Admin)", command=lambda: admin_login(show_results),
          bg="#8B0000", fg="white", font=("Helvetica", 11, "bold")).pack(pady=5)

tk.Button(root, text="Reset System (Admin)", command=lambda: admin_login(reset_votes),
          bg="#B22222", fg="white", font=("Helvetica", 11, "bold")).pack(pady=5)

root.mainloop()
