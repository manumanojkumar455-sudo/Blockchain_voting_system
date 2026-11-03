from flask import Flask, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)

# Create blockchain
voting_blockchain = Blockchain()

# Available candidates
candidates = ["Candidate A", "Candidate B", "Candidate C"]

# Store voter IDs to prevent duplicate voting
voted_voters = set()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["GET", "POST"])
def vote():
    message = None
    success = False

    if request.method == "POST":
        voter_id = request.form.get("voter_id", "").strip()
        candidate = request.form.get("candidate", "")

        if not voter_id:
            message = "Please enter your voter ID."

        elif voter_id in voted_voters:
            message = "This voter ID has already voted."

        elif candidate not in candidates:
            message = "Please select a valid candidate."

        else:
            voting_blockchain.add_block({
                "voter": voter_id,
                "candidate": candidate
            })

            voted_voters.add(voter_id)

            return redirect(url_for("results"))

    return render_template(
        "vote.html",
        candidates=candidates,
        message=message,
        success=success
    )


@app.route("/results")
def results():
    vote_counts = {candidate: 0 for candidate in candidates}

    for block in voting_blockchain.chain:
        if isinstance(block.data, dict):
            candidate = block.data.get("candidate")

            if candidate in vote_counts:
                vote_counts[candidate] += 1

    total_votes = sum(vote_counts.values())

    chain_valid = voting_blockchain.is_chain_valid()

    return render_template(
        "results.html",
        vote_counts=vote_counts,
        total_votes=total_votes,
        chain_valid=chain_valid
    )


@app.route("/blockchain")
def blockchain():
    return render_template(
        "blockchain.html",
        chain=voting_blockchain.chain,
        chain_valid=voting_blockchain.is_chain_valid()
    )


if __name__ == "__main__":
    app.run(debug=True)