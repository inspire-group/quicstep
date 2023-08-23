import csv
import pickle
import requests

if __name__ == '__main__':
    h3_domains = []
    i = 0

    # measure HTTP/3 support from first 10K domains of Majestic Million domain list
    with open('comps/demos/quic-migrate/evaluate/majestic_million.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            domain = f'https://{row["Domain"]}'
            print(domain)
            i += 1
            
            if i == 10001:
                break
            
            try:
                response = requests.get(domain, timeout=10)
            except:
                continue

            if "h3" in response.headers.get("Alt-Svc", ""):
                h3_domains.append(domain)

    # dump HTTP/3 domains to pkl for later usage
    with open('h3_domains.pkl', 'wb') as f:
        pickle.dump(h3_domains, f)