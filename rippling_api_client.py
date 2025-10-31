"""
Rippling API Client for Capitol Engineering (capitolaz.com)
Time tracking integration for project labor monitoring

This module provides a client to interact with Rippling's API to pull
employee time tracking data for project management and foreman monitoring.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class RipplingAPIClient:
    """Client for interacting with Rippling REST API"""

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Rippling API client

        Args:
            api_token: Rippling API token. If not provided, will look for RIPPLING_API_TOKEN env var
        """
        self.api_token = api_token or os.getenv('RIPPLING_API_TOKEN')
        if not self.api_token:
            raise ValueError("API token must be provided or set in RIPPLING_API_TOKEN environment variable")

        self.base_url = "https://rest.ripplingapis.com"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                     data: Optional[Dict] = None) -> Dict:
        """
        Make an authenticated request to the Rippling API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            data: Request body data

        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise

    def get_employees(self, limit: int = 100) -> List[Dict]:
        """
        Get list of all employees

        Args:
            limit: Maximum number of results per page (default 100)

        Returns:
            List of employee dictionaries
        """
        employees = []
        cursor = None

        while True:
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor

            response = self._make_request('GET', '/users', params=params)

            employees.extend(response.get('data', []))

            # Check for next page
            cursor = response.get('next_cursor')
            if not cursor:
                break

        return employees

    def get_time_entries(self, start_date: Optional[str] = None,
                        end_date: Optional[str] = None,
                        limit: int = 100) -> List[Dict]:
        """
        Get time entries for a date range

        Args:
            start_date: Start date in YYYY-MM-DD format (defaults to today)
            end_date: End date in YYYY-MM-DD format (defaults to today)
            limit: Maximum number of results per page

        Returns:
            List of time entry dictionaries
        """
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        time_entries = []
        cursor = None

        while True:
            params = {
                'limit': limit,
                'start_date': start_date,
                'end_date': end_date
            }
            if cursor:
                params['cursor'] = cursor

            # Note: The exact endpoint may vary - check Rippling documentation
            # Common endpoints: /time-entries or /time_tracking/entries
            response = self._make_request('GET', '/time-entries', params=params)

            time_entries.extend(response.get('data', []))

            cursor = response.get('next_cursor')
            if not cursor:
                break

        return time_entries

    def get_job_dimensions(self) -> List[Dict]:
        """
        Get list of job dimensions (projects/cost centers)

        Returns:
            List of job dimension dictionaries
        """
        response = self._make_request('GET', '/job-dimensions')
        return response.get('data', [])

    def get_jobs_for_dimension(self, dimension_id: str) -> List[Dict]:
        """
        Get list of jobs for a specific dimension

        Args:
            dimension_id: ID of the job dimension

        Returns:
            List of job dictionaries
        """
        response = self._make_request('GET', f'/job-dimensions/{dimension_id}/jobs')
        return response.get('data', [])


def test_connection():
    """Test the API connection and print basic info"""
    try:
        client = RipplingAPIClient()
        print("✓ API client initialized successfully")

        # Test getting employees
        employees = client.get_employees(limit=5)
        print(f"✓ Successfully retrieved {len(employees)} employees (sample)")

        # Test getting time entries for today
        today = datetime.now().strftime('%Y-%m-%d')
        time_entries = client.get_time_entries(start_date=today, end_date=today)
        print(f"✓ Successfully retrieved {len(time_entries)} time entries for today")

        print("\nConnection test successful!")
        return True

    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
