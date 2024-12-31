# README for `simplify_numbers` Python Script

## Overview

This Python script simplifies and approximates numbers and percentages in a given text. It uses regular expressions (regex) to identify numeric values, percentages, temperatures (in °C), and date-related information (such as years and months). The script then applies specific rules to approximate these numbers and transform them into a more generalized form. 

### Key Features:
1. **Approximation of Numbers**: Numbers are approximated based on a defined threshold.
2. **Percentage Parsing**: Percentages are simplified into words like "wenige", "die Hälfte", "mehr als die Hälfte", etc.
3. **Temperature Conversion**: Temperatures (in °C) are approximated and prefixed with "etwa".
4. **Year/Month Handling**: Year/month information is temporarily masked to avoid confusion during number simplification.

---

## Code Walkthrough

### 1. **Regex Definitions**:

- **`integersRegex`**: Captures integers or decimal numbers, with optional commas or dots.
- **`percentRegex`**: Matches percentages (e.g., `25 Prozent`).
- **`tempRegex`**: Matches temperatures (e.g., `38.7 Grad Celsius`).
- **`yearsormonthsRegex`**: Matches years or months (e.g., `Januar 2024`).

### 2. **Approximation Functions**:

#### `approx(number, isNegative=False) -> str`
This function approximates a number based on the following rules:
- It considers both dot-separated decimals and comma-separated decimals.
- It checks if the decimals are greater than a threshold (`afDecimalthreshold`) and adjusts the number accordingly.
- The function handles both positive and negative numbers (by checking `isNegative`).

#### `approxMatch(match)`
This is a wrapper around `approx()` for use with regex matching, applying the approximation to the matched number.

#### `approxCelsiusMatch(match)`
This function handles temperature strings, removing the "Grad Celsius" part and returning an approximation with "etwa" (e.g., `etwa 39 Grad Celsius`).

#### `parsePercent(match) -> str`
This function converts a percentage (e.g., `25 Prozent`) into a descriptive form (e.g., `"jeder Vierte"`), based on the numeric value. It handles:
- Very low percentages (`wenige`).
- Special cases like 25%, 50%, 75%.
- High percentages (`fast alle`).

#### `convertToInt(number: str) -> int`
This helper function converts a number (possibly with decimal points) into an integer, shifting the decimal places appropriately.

### 3. **Text Processing Functions**:

#### `denymatch(match)`
This function temporarily masks year/month data (matched by `yearsormonthsRegex`) by replacing it with a placeholder (`"***********"`). This prevents year/month information from being altered during number processing.

#### `PutbackYearMonth(raw_text: str) -> str`
This function restores the original year/month information from the placeholder back into the text.

### 4. **Main Function**: `simplify_numbers(raw_text: str)`

This function orchestrates the entire process:
- It applies the regex-based functions in sequence to simplify the text:
  1. Parse and simplify percentages.
  2. Approximate temperatures.
  3. Mask and temporarily handle year/month data.
  4. Approximate numbers.
  5. Restore the year/month data to its original form.

---

## Usage

### Function: `simplify_numbers(raw_text: str)`

The main function that simplifies numbers and percentages in the provided text.

**Parameters**:
- `raw_text`: A string containing the text to be processed.

**Returns**:
- A string with approximated numbers, simplified percentages, and temperature conversions.

### Example:

```python
test_cases = [
    "324.620,22 Euro wurden gespendet.",
    "25 Prozent der Bevölkerung sind betroffen.",
    "Bei 38,7 Grad Celsius ist es sehr heiß.",
    "Im Jahr 2024 gab es 1.234 Ereignisse."
]

for case in test_cases:
    print(simplify_numbers(case))
```


---

## Limitations & Notes:
- The approximation uses a fixed threshold (`afDecimalthreshold = 0.5`), which may need adjustment depending on the desired precision.
- The regex patterns are designed to capture only specific formats (e.g., no support for numbers with commas without decimals).
- The year/month information is temporarily masked to avoid being altered, but the restoration process may not work perfectly in all scenarios.

---

## Requirements

- Python 3.x
- `re` module (part of Python's standard library)

---

This script is useful for text processing where numerical information needs to be simplified or approximated, especially in contexts like statistical reports or data summarization.