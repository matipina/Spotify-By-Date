from unittest import result


def get_saved_albums(sp, limit=50, offset=0, extra_items=[]):
    albums = sp.current_user_saved_albums(limit=limit, offset=offset)
    total = albums['total']
    items = albums['items']
    items += extra_items

    remaining = total - len(items)

    if remaining > 0:
        new_offset = len(items)
        items = get_saved_albums(sp, 50, new_offset, extra_items=items)
        return items

    else:
        return items

def display_results(albums):
    print(f'Got {len(albums)} albums')    

    i = 0
    results = ''
    for item in albums:
        i += 1
        album = item['album']
        
        name = album['name']
        artists = album['artists']
        artists_names = [a['name'] for a in artists]
        release_date = album['release_date']
        results += (f'[{i}] {name} - {artists_names[0]} ({release_date})\n')
    return results