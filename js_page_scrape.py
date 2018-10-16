from requests_html import HTMLSession

print('creating session...')
session = HTMLSession()
print('getting html...')
#r = session.get('https://www.bbc.co.uk/programmes/m0000pc1')
r = session.get('https://www.nts.live/')
print('rendering javascript...')
await r.html.render()
print('complete')