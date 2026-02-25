from datetime import datetime

# Task 1: Search the DB for existing links
def find_matching_contacts(cursor, email, phone):
    cursor.execute("SELECT * FROM Contact WHERE email = ? OR phoneNumber = ?", (email, phone))
    return cursor.fetchall()

# Task 2: Find the "Ultimate" primary IDs for all matches
def get_primary_contact(cursor, matches):
    # Find the ID of the primary for every record we found
    linked_ids = {row['id'] if row['linkPrecedence'] == 'primary' else row['linkedId'] for row in matches}

    # Fetch those primary records and sort by oldest first
    placeholders = ','.join(['?'] * len(linked_ids))
    cursor.execute(
        f"SELECT * FROM Contact WHERE id IN ({placeholders}) ORDER BY createdAt ASC", 
        list(linked_ids)
    )
    return cursor.fetchall()

# Task 3: Turn newer primaries into secondaries
def merge_primaries(cursor, primary_id, all_primaries):
    for p in all_primaries:
        # If the primary is not the oldest one, demote it
        if p['id'] != primary_id:
            cursor.execute(
                """UPDATE Contact SET linkPrecedence = 'secondary', 
                   linkedId = ?, updatedAt = CURRENT_TIMESTAMP 
                   WHERE id = ? OR linkedId = ?""", 
                (primary_id, p['id'], p['id'])
            )

# Task 4: Create a secondary record if the info is new
def add_new_secondary(cursor, primary_id, email, phone, matches):
    # Check if this specific email/phone combo already exists in our matches
    has_email = any(row['email'] == email for row in matches) if email else True
    has_phone = any(row['phoneNumber'] == phone for row in matches) if phone else True

    # If either piece of info is new, save it as a secondary link
    if not has_email or not has_phone:
        cursor.execute(
            "INSERT INTO Contact (email, phoneNumber, linkedId, linkPrecedence) VALUES (?, ?, ?, 'secondary')", 
            (email, phone, primary_id)
        )

# Task 5: Gather all related data for the JSON response
def get_consolidated_data(cursor, primary_id):
    cursor.execute(
        "SELECT * FROM Contact WHERE id = ? OR linkedId = ? ORDER BY createdAt ASC", 
        (primary_id, primary_id)
    )
    rows = cursor.fetchall()

    emails = []
    phones = []
    secondary_ids = []

    for row in rows:
        if row['email'] and row['email'] not in emails:
            emails.append(row['email'])
        if row['phoneNumber'] and row['phoneNumber'] not in phones:
            phones.append(row['phoneNumber'])
        if row['linkPrecedence'] == 'secondary':
            secondary_ids.append(row['id'])

    return {
        "contact": {
            "primaryContactId": primary_id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }

# THE MAIN ORCHESTRATOR
def reconcile_and_fetch(conn, email, phone):
    cursor = conn.cursor()
    
    # 1. Search for existing rows
    matches = find_matching_contacts(cursor, email, phone)

    if not matches:
        # Create a brand new primary user
        cursor.execute(
            "INSERT INTO Contact (email, phoneNumber, linkPrecedence) VALUES (?, ?, 'primary')", 
            (email, phone)
        )
        primary_id = cursor.lastrowid
    else:
        # 2. Get all involved primaries and pick the oldest
        primaries = get_primary_contact(cursor, matches)
        primary_id = primaries[0]['id']
        
        # 3. If multiple primaries exist, merge them into the oldest
        if len(primaries) > 1:
            merge_primaries(cursor, primary_id, primaries)
        
        # 4. If this request has new info, add it as a secondary
        add_new_secondary(cursor, primary_id, email, phone, matches)

    # Save changes and return final formatted data
    conn.commit()
    return get_consolidated_data(cursor, primary_id)