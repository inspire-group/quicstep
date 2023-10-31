import numpy as np
import matplotlib.pyplot as plt
import subprocess
import time

NUM_REQUESTS = 250
WG_INTERFACE = "wg0"

# get latency (ms) for requesting the desired server file
def get_latency_ms():
    before_time = time.perf_counter()
    subprocess.run(
        [
        'comps/demos/quic-migrate/chromium-src/src/out/Debug/quic_client', 
        '--host=3.237.62.162',
        '--port=6121',
        '--disable_certificate_verification', 
        '--quiet', 
        'https://www.example.org/file_1MB.dat'
        ]
    )
    after_time = time.perf_counter()

    return (after_time - before_time) * 1000

if __name__ == '__main__':
    vpn_latency = []
    naive_latency = []
    comps_latency = []
    
    for i in range(NUM_REQUESTS):
        subprocess.run(['sudo', './setup.sh'])
        comps_latency.append(get_latency_ms())
        subprocess.run(['sudo', './takedown.sh'])

        subprocess.run(['sudo', 'wg-quick', "up", WG_INTERFACE])
        vpn_latency.append(get_latency_ms())
        subprocess.run(['sudo', 'wg-quick', "down", WG_INTERFACE])

        naive_latency.append(get_latency_ms())

    vpn_latency = np.array(vpn_latency)
    naive_latency = np.array(naive_latency)
    comps_latency = np.array(comps_latency)

    vpn_values, vpn_base = np.histogram(vpn_latency, bins=50)
    vpn_cdf = np.cumsum(vpn_values / sum(vpn_values))

    naive_values, naive_base = np.histogram(naive_latency, bins=50)
    naive_cdf = np.cumsum(naive_values / sum(naive_values))

    comps_values, comps_base = np.histogram(comps_latency, bins=50)
    comps_cdf = np.cumsum(comps_values / sum(comps_values))

    plt.xlabel("Latency (ms)")
    plt.ylabel("Probability")
    plt.plot(vpn_base[1:], vpn_cdf, label="High Latency Secure Tunnel")
    plt.plot(naive_base[1:], naive_cdf, label="Censorship Vulnerable Native Link")
    plt.plot(comps_base[1:], comps_cdf, label="QUICstep Connection")
    plt.legend()
    plt.savefig("cdf.pdf")
