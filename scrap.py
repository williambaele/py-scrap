from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/getMemberId')
def get_member_id():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'Missing required parameter: id'}), 400
    
    try:
        url = f"https://tennis.tennispadelwalloniebruxelles.be/MyAFT/Players/Detail/{id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the element containing the memberId
        link = soup.find('a', {'data-target': '#tabPlayerFunctionsClub'})
        if link and 'data-url' in link.attrs:
            data_url = link['data-url']
            # Extract memberId from the data-url
            match = re.search(r'memberId=(\d+)', data_url)
            if match:
                member_id = match.group(1)
                return jsonify({'memberId': member_id}), 200
            else:
                return jsonify({'error': 'Member ID not found'}), 404
        else:
            return jsonify({'error': 'Member ID not found'}), 404

    except requests.RequestException as e:
        print(f"Error during crawling: {e}")
        return jsonify({'error': 'Failed to fetch Member ID due to server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
