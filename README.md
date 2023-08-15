
# OpenMRS REST API Client for Location Operations

This script, `omrs_locations_csv.py`, provides a simple REST client for interacting with the OpenMRS API, focusing on location-related operations using CSV input.

## Features

- **List Locations**: Fetches all locations from OpenMRS.
- **Add New Location**: Adds a new location to OpenMRS.
- **Update Existing Location**: Modifies details of an existing location in OpenMRS.
- **Command-Line Interface**: Supports various command-line arguments for easy configuration and usage.
- **CSV Parsing**: Parses location data from a CSV file to either add or update locations in OpenMRS.

## Requirements

1. **Python 3**
2. Python packages:
   - `requests`
   - `yaml`
  
   Install the required packages using:
   ```bash
   pip install requests pyyaml
   ```

## Usage

### Command Line Arguments

- **General Arguments**:
  - `--config, -c`: Path to the configuration file. Default is `omrs.yml`.
  - `--base_url, -b`: URL of OpenMRS API up to the version number (without the ending slash).
  - `--user, -u`: Username for API authentication. Default is `admin`.
  - `--pw, -p`: Password for API authentication. Default is `Admin123`.
  - `--quiet, -q`: Run the script quietly without verbose output.
  - `--csv, -csv`: Path to a CSV file containing location data.

- **Subcommands**:
  - `locations`: List locations.
  - `addlocation`: Add a new location. Requires `--name`. Optional: `--description`, `--tags`, `--country`, `--parentLocation`.
  - `updatelocation`: Update an existing location. Requires `--uuid`. Optional: `--name`, `--description`, `--tags`, `--country`, `--parentLocation`.

### Configuration File (`omrs.yml`)

For ease of use, the default configuration file is named `omrs.yml` and should contain:
```yaml
base_url: "YOUR_OPENMRS_API_URL"
user: "YOUR_USERNAME"
pw: "YOUR_PASSWORD"
```
Replace placeholders with appropriate details.

### CSV Format

If providing a CSV file for location data, the script expects:
- `UUID`: Unique identifier for the location.
- `name`: Name of the location.
- `Description`: (Optional) Description of the location.
- `Tags`: (Optional) Comma-separated tags for the location.
- `Country`: (Optional) Country of the location.
- `ParentLocation`: (Optional) Parent location name.

**Note**: CSV delimiter is `;`.

### Examples

1. **List Locations**:
   ```bash
   python omrs_locations_csv.py locations
   ```

2. **Add New Location**:
   ```bash
   python omrs_locations_csv.py addlocation --name "New Location" --description "This is a new location."
   ```

3. **Update Existing Location**:
   ```bash
   python omrs_locations_csv.py updatelocation --uuid "LOCATION_UUID" --name "Updated Location Name"
   ```

4. **Process Locations from CSV**:
   ```bash
   python omrs_locations_csv.py --csv "path_to_file.csv"
   ```

## Conclusion

`omrs_locations_csv.py` offers a convenient interface to interact with the OpenMRS API for location-related tasks. Ensure that your OpenMRS instance and API are properly set up and accessible before using this script.




