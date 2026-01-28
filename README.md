# eBird Alert Scraper

An automated web scraper that fetches notable bird observations from eBird and displays them on a beautiful interactive GitHub Pages site. The scraper runs every 6 hours via GitHub Actions and maintains historical data.

## Features

- Automatically scrapes notable bird observations from eBird API
- Runs every 6 hours via GitHub Actions
- Stores historical data to track changes over time
- Beautiful interactive table with filtering and sorting
- Responsive design that works on mobile and desktop
- Shows real-time statistics (total observations, unique species, etc.)
- Separate views for latest and historical data

## Live Demo

Once deployed, your site will be available at: `https://[your-username].github.io/ebird-scraper/`

## Setup Instructions

### 1. Get an eBird API Key

1. Go to [eBird.org](https://ebird.org)
2. Log in or create an account
3. Request an API key from your account settings
4. Save this key - you'll need it in step 4

### 2. Create a GitHub Repository

1. Create a new repository on GitHub (name it `ebird-scraper` or any name you prefer)
2. Set it to **Public** (required for GitHub Pages)
3. Don't initialize with README (we already have one)

### 3. Push Code to GitHub

In your terminal, run these commands from the project directory:

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ebird-scraper.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: eBird scraper with GitHub Pages"

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Add eBird API Key as GitHub Secret

1. Go to your repository on GitHub
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `EBIRD_API_KEY`
5. Value: Paste your eBird API key
6. Click **Add secret**

### 5. Enable GitHub Pages

1. Go to **Settings** > **Pages**
2. Under **Source**, select **GitHub Actions**
3. Save

### 6. Run the Scraper

The scraper will run automatically every 6 hours, but you can trigger it manually:

1. Go to **Actions** tab
2. Click on **Scrape eBird Data and Deploy**
3. Click **Run workflow** > **Run workflow**

Wait a few minutes for the workflow to complete. Your site will be live!

## Configuration

### Change the Hotspot or Region

Edit [scraper.py](scraper.py:18) and change the `HOTSPOT_ID` variable:

```python
HOTSPOT_ID = 'SN35466'  # Change this to your desired hotspot ID
```

You can find hotspot IDs from eBird URLs, or use region codes like:
- Country: `US`
- State/Province: `US-CA`
- County: `US-CA-037`

### Change Scraping Frequency

Edit [.github/workflows/scrape-and-deploy.yml](.github/workflows/scrape-and-deploy.yml:7) and modify the cron schedule:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

Cron syntax:
- `0 */1 * * *` - Every hour
- `0 */3 * * *` - Every 3 hours
- `0 0 * * *` - Daily at midnight
- `0 0,12 * * *` - Twice daily (midnight and noon)

### Change Days Back for Observations

Edit [scraper.py](scraper.py:60) in the `fetch_notable_observations` function:

```python
def fetch_notable_observations(hotspot_id: str, days_back: int = 7):
```

Change `days_back=7` to your preferred number of days.

## Project Structure

```
ebird-scraper/
├── .github/
│   └── workflows/
│       └── scrape-and-deploy.yml  # GitHub Actions workflow
├── data/
│   ├── latest.json                # Latest scrape data
│   └── historical.json            # All historical scrapes
├── docs/
│   └── index.html                 # GitHub Pages website
├── scraper.py                     # Main scraper script
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## How It Works

1. **GitHub Actions** triggers the workflow every 6 hours (or on manual trigger)
2. **Scraper** (`scraper.py`) fetches notable observations from eBird API
3. **Data Storage** saves observations to `data/latest.json` and appends to `data/historical.json`
4. **Git Commit** automatically commits the updated data files
5. **Deployment** GitHub Actions deploys the `docs` folder to GitHub Pages
6. **Website** displays the data in an interactive, filterable table

## API Reference

This project uses the [eBird API 2.0](https://documenter.getpostman.com/view/664302/S1ENwy59).

Key endpoints used:
- `GET /data/obs/{regionCode}/recent/notable` - Recent notable observations

## Troubleshooting

### Scraper fails with 401 error
- Check that your `EBIRD_API_KEY` secret is set correctly in GitHub

### Scraper fails with 404 error
- Verify the hotspot ID is correct
- Try using a region code instead of a hotspot ID

### GitHub Pages shows old data
- Check that the workflow completed successfully in the Actions tab
- Clear your browser cache
- Wait a few minutes for GitHub Pages to update

### No data appears on the website
- The scraper needs to run at least once to generate data files
- Manually trigger the workflow from the Actions tab
- Check the workflow logs for any errors

## Local Development

To run the scraper locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export EBIRD_API_KEY='your-key-here'

# Run the scraper
python scraper.py

# View the website locally
cd docs
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

## Contributing

Feel free to open issues or submit pull requests with improvements!

## License

MIT License - feel free to use this project for your own eBird monitoring needs.

## Credits

- Data provided by [eBird](https://ebird.org)
- Built with Python, GitHub Actions, and vanilla JavaScript
- Uses [DataTables](https://datatables.net/) for interactive tables

## Resources

- [eBird API Documentation](https://documenter.getpostman.com/view/664302/S1ENwy59)
- [eBird Alerts Help](https://support.ebird.org/en/support/solutions/articles/48000960317-ebird-alerts-and-targets-faqs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
