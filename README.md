# KALE Price Tracker

## Overview
KALE Price Tracker is a Python-based application that fetches real-time KALE token prices using the Stellar Testnet Horizon API, integrated with the Reflector oracle. It leverages the official KALE issuing key (`GCHPTWXMT3HYF4RLZHWBNRF4MPXLTJ76ISHMSYIWCCDXWUYOQG5MR2AB`) to query trades. The project features console output, price logging to a file (`kale_price_log.txt`), and a visual price trend graph using `matplotlib`. For reliable demos, it includes fallbacks to CSV (`test_prices.csv`) and hard-coded data when Testnet trades are unavailable. This is a minimal viable product (MVP) designed for the Stellar Hacks: KALE x Reflector hackathon, extensible for DeFi applications.

## Setup
1. Install Python 3.13 (or 3.8+).
2. Install dependencies: `py -m pip install stellar-sdk pandas matplotlib`.
3. Place `test_prices.csv` in the project directory (included in this repository).
4. Run the script: `py price_tracker.py`.

## Output
- **Console**: Real-time KALE prices from Testnet, CSV, or hard-coded data.
- **Log File**: `kale_price_log.txt` stores price history with timestamps.
- **Graph**: Visual price trend displayed using `matplotlib` after 5 measurements.

## Files
- `price_tracker.py`: Main script for fetching and visualizing KALE prices.
- `test_prices.csv`: Fallback test data for demo reliability.
- `kale_price_log.txt`: Generated log file with price history.
- `demo_screenshot.png`: Sample screenshot of console output and graph.

## Notes
- Built with `stellar-sdk` v13.0.0 for Stellar Testnet integration.
- Uses KALE issuing key for direct relevance to the hackathon.
- Fallback mechanisms ensure robust demos even without live Testnet trades.
- Future extensions include UI integration, smart contract support, or multi-asset tracking.

## License
Apache-2.0
