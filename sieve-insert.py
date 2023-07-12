import json
import sys
import subprocess

def update_json(domains, file_data):
    for new_domain in domains:
        if new_domain not in file_data["domains"]:
            file_data["domains"].append(new_domain)
        else:
            print(F"{new_domain} already present")
    file_data["domains"] = sorted(file_data["domains"])
    return file_data


def write_sieve(updated_file_data):
    domains_formatted =', '.join('"{0}"'.format(domain) for domain in updated_file_data['domains'])
    sieve = F'require ["include", "environment", "variables", "relational", "comparator-i;ascii-numeric", "spamtest"]; if allof (address :all :comparator "i;unicode-casemap" :contains "From" [{domains_formatted}] ) {{ discard; }} '
    with open('blocklist.sieve', 'w') as f:
        f.write(sieve)


def write_json(domains, filename='sieve-blocklist.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)

        updated_file_data = update_json(domains, file_data)
        write_sieve(updated_file_data)

        file.seek(0)
        json.dump(updated_file_data, file, indent = 4)
        return 1
 

if __name__ == '__main__':
    domains = sys.argv
    domains.pop(0) # remove filename from list
    if (write_json(domains)):
        subprocess.call(['sh', './anon-commit-push.sh']) 
