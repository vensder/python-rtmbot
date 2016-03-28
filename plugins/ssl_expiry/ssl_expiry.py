import socket
import ssl
import datetime
import re

outputs = []

trigger_phrase = '@ssl date'
#trigger_phrase_to_run = '@ssl date'


def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt) # 2016-04-19 23:59:59 # <class 'datetime.datetime'>

# emoji
# :white_check_mark:
# :warning:


def process_message(data):
    
    # default domain name
    domain = 'google.com'
    
    if 'text' in data:
        try:
            text = data['text']
            channel = data['channel']

            trigger = re.compile(trigger_phrase)
            if trigger.match(text):
                string_with_domain = trigger.split(text)[1] # rest of text without trigger phrase
                
                mask = re.compile(r'([A-Za-z0-9-]+\.)+\w+') # domain pattern
                if mask.search(string_with_domain):
                    search_domain = mask.search(string_with_domain)
                    domain = search_domain.group()
                    
                    print(domain); print(type(domain))
                    
                    try:
                        expiry_datetime = ssl_expiry_datetime(domain)
                        now = datetime.datetime.now()
                        delta = expiry_datetime - now
                        
                        emoji = ':white_check_mark:'
                        if delta.days < 30:
                            emoji = ':warning:'
                        output_string = 'Certificate for domain ' + domain + ' will expire in ' + str(delta.days) + ' days (' + str(expiry_datetime) + ')'
                        print(output_string)
                        outputs.append([channel, output_string, 'SSL checker', emoji ])
                        
                    except Exception as e:
                        emoji = ':exclamation:'
                        outputs.append([data['channel'], str(e) + ': ' + domain, 'SSL checker', emoji ])
                        print('Exception in ssl plugin: ',e)
                        print('network: ', domain)
                        
                

        except KeyError as e:
            print('KeyError Exception: ', e)
