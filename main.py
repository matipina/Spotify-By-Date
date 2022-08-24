import requests
import sys

USER_ID = '12137742447'
SPOTIFY_CREATE_PLAYLIST_URL = f'https://api.spotify.com/v1/users/{USER_ID}/playlists'
SPOTIFY_GET_ALBUMS_URL = f'https://api.spotify.com/v1/me/albums'
ACCESS_TOKEN = \
    'BQC8ICC9XqdzqubmhVtgZhKc4EyUCKo8g6NroGqXuhX9seG0fo8rwqlJl_Q3ipSqxS_7Bvv3Ub3QgCF34vP4OTW3rG5H51FfUmREPq0V5jCknmG5wrwCOit9Gid4m3_JFl08RrZpZq9joj-cgMEhvtO9nuslvEcHKRktHtqqpUpX4krlQtJ1LwW--nBp5w'
def create_playlist(name, public=False):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={
            'Authorization': f"Bearer {ACCESS_TOKEN}"
        },
        json={
            'name': name,
            'public': public
        }
    )

    json_resp = response.json()

    return json_resp

def get_saved_albums(limit=50, offset=0, extra_items=[]):
    query = {
        'limit': limit,
        'offset': offset
    }
    headers = {
        'Authorization': f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(
        SPOTIFY_GET_ALBUMS_URL,
        headers=headers,
        params=query
    )
    json_resp = response.json()

    if response.status_code == 200:
        albums = json_resp
        total = albums['total']
        items = albums['items']
        items += extra_items

        remaining = total - len(items)

        if remaining > 0:
            new_offset = len(items)
            
            items = get_saved_albums(50, new_offset, extra_items=items)
            return items

        else:
            return items
    else:
        print(response.status_code)

def display_results(albums):
    print(f'Got {len(albums)} albums')    

    i = 0
    for item in albums:
        i += 1
        album = item['album']
        
        name = album['name']
        artists = album['artists']
        artists_names = [a['name'] for a in artists]
        release_date = album['release_date']
        print(f'[{i}] {name} - {artists_names[0]} ({release_date})')

def main(year):
    print(f'year: {year}')
    albums = get_saved_albums()

    if year:
        filtered_albums = [item for item in albums if item['album']['release_date'][:4] == year]
        display_results(filtered_albums)
 
    else:
        display_results(albums)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input = sys.argv[1]
    else:
        input = None
    main(input)