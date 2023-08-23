import pickle
import subprocess

if __name__ == "__main__":
    firefox_domains = []

    with open('h3_domains.pkl', 'rb') as f:
        h3_domains = pickle.load(f)

    subprocess.run(['sudo', './setup.sh'])

    for domain in h3_domains:
        output = subprocess.run(
            [
            'target/debug/neqo-client',
            domain,
            ],
            capture_output=True,
        )
        if b'READ' in output.stdout:
            firefox_domains.append(domain)

    with open('firefox_migration_domains.pkl', 'wb') as f:
        pickle.dump(firefox_domains, f)

    print(len(h3_domains))
    print(len(firefox_domains))
    print("Total Domains: 10000")

    subprocess.run(['sudo', './takedown.sh'])
