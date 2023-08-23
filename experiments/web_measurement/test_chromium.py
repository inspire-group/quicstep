import pickle
import subprocess

if __name__ == "__main__":
    chromium_domains = []

    with open('h3_domains.pkl', 'rb') as f:
        h3_domains = pickle.load(f)

    subprocess.run(['sudo', './setup.sh'])

    for domain in h3_domains:
        output = subprocess.run(
            [
            'comps/demos/quic-migrate/chromium-src/src/out/Debug/quic_client', 
            '--disable_certificate_verification', 
            '--quiet', 
            domain,
            ],
            capture_output=True,
        )
        if output.stdout:
            chromium_domains.append(domain)

    with open('chromium_migration_domains.pkl', 'wb') as f:
        pickle.dump(chromium_domains, f)

    print(len(h3_domains))
    print(len(chromium_domains))
    print("Total Domains: 10000")

    subprocess.run(['sudo', './takedown.sh'])