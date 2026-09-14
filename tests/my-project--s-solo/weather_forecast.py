#!/usr/bin/env python3
"""
Fetch tomorrow's hourly weather forecast from Open-Meteo for a configurable time slot.
Usage: python3 weather_forecast.py [--lat LAT] [--lon LON] [--from-hour H] [--to-hour H]
"""
from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import date, timedelta

WMO_DESCRIPTIONS = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icing fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Heavy thunderstorm with hail",
}


def fetch_forecast(lat: float, lon: float) -> dict:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation,weathercode"
        f"&forecast_days=2"
        f"&timezone=auto"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())


def filter_tomorrow(data: dict, from_hour: int, to_hour: int) -> list[dict]:
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    precips = data["hourly"]["precipitation"]
    codes = data["hourly"]["weathercode"]

    rows = []
    for i, t in enumerate(times):
        if not t.startswith(tomorrow):
            continue
        hour = int(t[11:13])
        if from_hour <= hour <= to_hour:
            rows.append({
                "time": t[11:16],
                "temp": temps[i],
                "precip": precips[i],
                "desc": WMO_DESCRIPTIONS.get(codes[i], f"Code {codes[i]}"),
            })
    return rows


def print_table(rows: list[dict], unit: str) -> None:
    if not rows:
        print("No data for this time slot.")
        return
    print(f"{'Time':>6}  {'Temp':>8}  {'Precip':>8}  Description")
    print("-" * 52)
    for r in rows:
        print(f"{r['time']:>6}  {r['temp']:>6.1f}{unit}  {r['precip']:>6.1f}mm  {r['desc']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tomorrow's weather forecast for a time slot.")
    parser.add_argument("--lat", type=float, default=48.8566, help="Latitude (default: Paris)")
    parser.add_argument("--lon", type=float, default=2.3522, help="Longitude (default: Paris)")
    parser.add_argument("--from-hour", type=int, default=8, metavar="H", help="Start hour 0-23 (default: 8)")
    parser.add_argument("--to-hour", type=int, default=10, metavar="H", help="End hour 0-23 (default: 10)")
    args = parser.parse_args()

    if not (0 <= args.from_hour <= 23 and 0 <= args.to_hour <= 23 and args.from_hour <= args.to_hour):
        parser.error("Hours must be in 0-23 and from-hour <= to-hour")

    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Forecast for {tomorrow} — {args.from_hour:02d}h to {args.to_hour:02d}h "
          f"(lat={args.lat}, lon={args.lon})\n")

    data = fetch_forecast(args.lat, args.lon)
    unit = data.get("hourly_units", {}).get("temperature_2m", "°C")
    print(f"\n{data}\n")
    rows = filter_tomorrow(data, args.from_hour, args.to_hour)
    print_table(rows, unit)


if __name__ == "__main__":
    main()
