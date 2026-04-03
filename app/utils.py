import csv

def export_csv(data, filename="transactions.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # header
        writer.writerow(["id", "amount", "type", "category", "date", "notes", "user_id"])

        # rows
        for t in data:
            writer.writerow([
                t.id,
                t.amount,
                t.type,
                t.category,
                t.date,
                t.notes,
                t.user_id
            ])

    return filename