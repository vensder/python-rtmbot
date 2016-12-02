import re

outputs = []

trigger_phrase = '@ssl get'
#trigger_phrase_to_run = '@ssl get'
#PATTERNS=( '^\w+\.overl\.ai\.coffee' '^\w+\.ehr\.works\.run' '^\w+\.staging\.visitnow.\org' )

def process_message(data):
    
    # default domain name
    domain = 'google.com'
    
    if 'text' in data and data['text']:
        try:
            text = data['text']
            channel = data['channel']

            trigger = re.compile(trigger_phrase)
            if trigger.match(text):
                string_with_domain = trigger.split(text)[1] # rest of text without trigger phrase

                mask_overlay = re.compile(r'[\w-]+\.overl\.ai\.coffee') # precompile pattern for <subdomain>.overl.ai.coffee
                mask_ehr = re.compile(r'[\w-]+\.ehr\.works\.run') # precompile pattern for <subdomain>.ehr.works.run
                mask_visit = re.compile(r'[\w-]+\.staging\.visitnow\.org') # precompile pattern for <subdomain>.staging.visitnow.org

                if mask_overlay.search(string_with_domain):
                    search_domain = mask_overlay.search(string_with_domain)
                    domain = search_domain.group()
                    # TODO send to Jeknins command to get ssl for overl.ai.coffee subdomain

                if mask_ehr.search(string_with_domain):
                    search_domain = mask_ehr.search(string_with_domain)
                    domain = search_domain.group()
                    # TODO send request to Jenkins for run gettin ssl for ehr.works.run subdomain

                if mask_visit.search(string_with_domain):
                    search_domain = mask_visit.search(string_with_domain)
                    domain = search_domain.group()
                    # TODO send requset to Jenkins for getting ssl for staging.visitnow.org subdomain

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
