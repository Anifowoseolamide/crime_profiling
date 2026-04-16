/**
 * Utility to fetch current device coordinates using browser Geolocation API.
 * Returns a promise that resolves to {lat, lng} or null if denied/failed.
 */
export const getCurrentLocation = () => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      console.warn('Geolocation is not supported by this browser.');
      resolve(null);
      return;
    }

    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
      },
      (error) => {
        console.error('Error fetching location:', error.message);
        resolve(null);
      },
      options
    );
  });
};
