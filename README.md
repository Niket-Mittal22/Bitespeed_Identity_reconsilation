**Project Overview**
This service is a backend system designed to solve the "Identity Fragmentation" problem. In e-commerce, a single user might make purchases using different emails or phone numbers at different times.

This API identifies these overlapping contact points and links them into a single "Primary" identity. It ensures that businesses see a unified view of their customers rather than multiple disconnected accounts.

**Tech Stack**
Language: Python 3.x

Web Framework: Flask (Lightweight and fast)

Database: SQLite (Relational storage for linking contacts)

Tooling: Postman (for API testing)


**Key Features & Logic**
1. The system follows a modular "Search-Merge-Link" architecture:

2. Search: Scans the database for any existing email or phone number matches.

3. Primary Identification: Automatically determines the "Ultimate Primary" based on the oldest account creation date.

4. Automatic Merging: If a request links two previously separate primary accounts, the system demotes the newer one to a secondary status.

5. Data Consolidation: Returns a nested JSON response containing all unique emails, phone numbers, and secondary IDs associated with the user.

**Setup Instructions**
1. Clone the repository
   git clone https://github.com/Niket-Mittal22/Bitespeed_Identity_reconsilation.git
   cd Bitespeed_Identity_reconsilation
2. Set up a Virtual Environment (Recommended)
   python -m venv venv
   venv\Scripts\activate
3. Install Dependencies
   pip install flask
4. Initialize the Database
   python init_db.py
5. Run the Server
   python app.py

The server will start at http://localhost:3000


      
