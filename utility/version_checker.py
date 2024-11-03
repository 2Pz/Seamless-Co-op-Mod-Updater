# version_checker.py
import pefile
import re

def extract_version_after_marker(filename, marker):
    """
    Extracts version information from a DLL file after a specified marker.

    Parameters:
        filename (str): Path to the DLL file.
        marker (str): Marker string to search for.

    Returns:
        str or None: Extracted version string, or None if not found.
    """
    try:
        pe = pefile.PE(filename)
        data_combined = b""

        # Combine data from all sections
        for section in pe.sections:
            data_combined += section.get_data()

        # Convert combined data to a string
        data_string = data_combined.decode('utf-8', errors='ignore')

        # Find the position of the marker
        marker_index = data_string.find(marker)

        # If the marker is found, extract the string after it
        if marker_index != -1:
            # Extract substring after the marker
            substring_after_marker = data_string[marker_index + len(marker):]

            # Use regex to find the version number pattern
            version_match = re.search(r'(\d+\.\s*\d+\.\s*\d+)', substring_after_marker)

            pe.close()  # Close the PE file

            if version_match:
                return version_match.group(0).strip()  # Return the version number
            else:
                return None
        else:
            pe.close()  # Close the PE file
            return None
    except Exception as e:
        print(f"Error extracting version: {e}")
        return None