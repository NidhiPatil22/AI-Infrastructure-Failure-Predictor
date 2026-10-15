import { useEffect, useRef, useState } from 'react';

// Curated Major Indian Corridors & Landmarks for instant selection and testing
const FALLBACK_CORRIDORS = [
  {
    name: 'Bandra-Worli Sea Link',
    city: 'Mumbai',
    state: 'Maharashtra',
    address: 'Bandra-Worli Sea Link, Mumbai, Maharashtra 400050, India',
    latitude: 19.033,
    longitude: 72.8164,
    type: 'Bridge',
  },
  {
    name: 'Mumbai - Pune Expressway',
    city: 'Pune',
    state: 'Maharashtra',
    address: 'Mumbai - Pune Expressway, Lonavala-Khandala, Maharashtra 410401, India',
    latitude: 18.756,
    longitude: 73.4116,
    type: 'Road',
  },
  {
    name: 'Atal Setu (MTHL)',
    city: 'Navi Mumbai',
    state: 'Maharashtra',
    address: 'Mumbai Trans Harbour Link (Atal Setu), Sewri-Nhava Sheva, Maharashtra, India',
    latitude: 18.995,
    longitude: 72.964,
    type: 'Bridge',
  },
  {
    name: 'Outer Ring Road (ORR)',
    city: 'Bengaluru',
    state: 'Karnataka',
    address: 'Outer Ring Road, Bellandur, Bengaluru, Karnataka 560103, India',
    latitude: 12.9279,
    longitude: 77.6833,
    type: 'Road',
  },
  {
    name: 'Durgam Cheruvu Cable Bridge',
    city: 'Hyderabad',
    state: 'Telangana',
    address: 'Durgam Cheruvu Cable Bridge, Hitec City, Hyderabad, Telangana 500081, India',
    latitude: 17.4334,
    longitude: 78.3872,
    type: 'Bridge',
  },
  {
    name: 'Yamuna Expressway',
    city: 'Greater Noida',
    state: 'Uttar Pradesh',
    address: 'Yamuna Expressway, Greater Noida to Agra, Uttar Pradesh 201310, India',
    latitude: 27.8974,
    longitude: 77.5298,
    type: 'Road',
  },
  {
    name: 'Vidyasagar Setu',
    city: 'Kolkata',
    state: 'West Bengal',
    address: 'Vidyasagar Setu, Toll Plaza, Kolkata, West Bengal 700021, India',
    latitude: 22.5562,
    longitude: 88.3277,
    type: 'Bridge',
  },
  {
    name: 'Samruddhi Mahamarg',
    city: 'Nagpur',
    state: 'Maharashtra',
    address: 'Hindu Hrudaysamrat Balasaheb Thackeray Maharashtra Samruddhi Mahamarg, Maharashtra, India',
    latitude: 20.3892,
    longitude: 78.1307,
    type: 'Road',
  },
  {
    name: 'Chennai Bypass Corridor',
    city: 'Chennai',
    state: 'Tamil Nadu',
    address: 'Chennai Bypass Road, Porur-Tambaram, Chennai, Tamil Nadu 600116, India',
    latitude: 13.0475,
    longitude: 80.1415,
    type: 'Road',
  },
  {
    name: 'Ahmedabad - Vadodara Expressway',
    city: 'Ahmedabad',
    state: 'Gujarat',
    address: 'National Expressway 1, Anand-Nadiad, Gujarat 387001, India',
    latitude: 22.5645,
    longitude: 72.9289,
    type: 'Road',
  },
];

export default function GoogleCorridorMap({ selectedLocation, onLocationSelect }) {
  const mapContainerRef = useRef(null);
  const searchInputRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markerInstanceRef = useRef(null);

  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '';
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [customLat, setCustomLat] = useState(selectedLocation?.latitude || 18.756);
  const [customLng, setCustomLng] = useState(selectedLocation?.longitude || 73.4116);
  const [customAddress, setCustomAddress] = useState(
    selectedLocation?.address || 'Mumbai - Pune Expressway, Maharashtra, India'
  );
  const [isConfirmed, setIsConfirmed] = useState(true);

  // Sync state if selectedLocation prop changes from parent
  useEffect(() => {
    if (selectedLocation) {
      if (selectedLocation.address) setCustomAddress(selectedLocation.address);
      if (selectedLocation.latitude) setCustomLat(selectedLocation.latitude);
      if (selectedLocation.longitude) setCustomLng(selectedLocation.longitude);
    }
  }, [selectedLocation]);

  // Load Google Maps API script if API key is provided
  useEffect(() => {
    if (!apiKey) {
      setLoadError(false); // Clean fallback mode
      return;
    }

    if (window.google && window.google.maps) {
      setMapsLoaded(true);
      return;
    }

    // Check if script is already added
    const existingScript = document.getElementById('google-maps-script');
    if (!existingScript) {
      const script = document.createElement('script');
      script.id = 'google-maps-script';
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setMapsLoaded(true);
      script.onerror = () => {
        console.warn('Google Maps script failed to load. Falling back to regional corridor selector.');
        setLoadError(true);
      };
      document.head.appendChild(script);
    } else {
      existingScript.addEventListener('load', () => setMapsLoaded(true));
      existingScript.addEventListener('error', () => setLoadError(true));
    }
  }, [apiKey]);

  // Initialize interactive Google Map once script is loaded
  useEffect(() => {
    if (!mapsLoaded || !mapContainerRef.current || !window.google || !window.google.maps) return;

    try {
      const defaultCenter = {
        lat: selectedLocation?.latitude || 18.756,
        lng: selectedLocation?.longitude || 73.4116,
      };

      const map = new window.google.maps.Map(mapContainerRef.current, {
        center: defaultCenter,
        zoom: 14,
        mapTypeId: 'roadmap',
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
        zoomControl: true,
        styles: [
          { elementType: 'geometry', stylers: [{ color: '#162230' }] },
          { elementType: 'labels.text.stroke', stylers: [{ color: '#162230' }] },
          { elementType: 'labels.text.fill', stylers: [{ color: '#cbd5e1' }] },
          { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#25374e' }] },
          { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ color: '#1a2737' }] },
          { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#fecb00' }] },
          { featureType: 'road.highway', elementType: 'geometry.stroke', stylers: [{ color: '#d99b00' }] },
          { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#09111c' }] },
        ],
      });
      mapInstanceRef.current = map;

      // Marker
      const marker = new window.google.maps.Marker({
        position: defaultCenter,
        map,
        title: selectedLocation?.address || 'Selected Infrastructure Location',
        animation: window.google.maps.Animation.DROP,
        draggable: true,
      });
      markerInstanceRef.current = marker;

      // Geocoder
      const geocoder = new window.google.maps.Geocoder();

      // Reverse geocode helper
      const updateFromLatLng = (lat, lng) => {
        geocoder.geocode({ location: { lat, lng } }, (results, status) => {
          let addr = `Coordinates: ${lat.toFixed(4)}, ${lng.toFixed(4)}, India`;
          let city = 'Pune';
          let state = 'Maharashtra';
          let postal = '';
          let placeId = null;

          if (status === 'OK' && results && results[0]) {
            addr = results[0].formatted_address;
            placeId = results[0].place_id;
            for (const comp of results[0].address_components) {
              if (comp.types.includes('locality')) city = comp.long_name;
              if (comp.types.includes('administrative_area_level_1')) state = comp.long_name;
              if (comp.types.includes('postal_code')) postal = comp.long_name;
            }
          }

          const locObj = {
            address: addr,
            latitude: lat,
            longitude: lng,
            city,
            state,
            postal_code: postal,
            place_id: placeId,
          };
          setCustomAddress(addr);
          setCustomLat(lat);
          setCustomLng(lng);
          setIsConfirmed(true);
          onLocationSelect(locObj);
        });
      };

      // Map click listener -> places marker & reverse geocodes
      map.addListener('click', (e) => {
        const lat = e.latLng.lat();
        const lng = e.latLng.lng();
        marker.setPosition(e.latLng);
        updateFromLatLng(lat, lng);
      });

      // Marker drag listener
      marker.addListener('dragend', (e) => {
        const lat = e.latLng.lat();
        const lng = e.latLng.lng();
        updateFromLatLng(lat, lng);
      });

      // Places Autocomplete
      if (searchInputRef.current && window.google.maps.places) {
        const autocomplete = new window.google.maps.places.Autocomplete(searchInputRef.current, {
          componentRestrictions: { country: 'in' },
          fields: ['formatted_address', 'geometry', 'name', 'place_id', 'address_components'],
        });

        autocomplete.addListener('place_changed', () => {
          const place = autocomplete.getPlace();
          if (!place.geometry || !place.geometry.location) return;

          map.setCenter(place.geometry.location);
          map.setZoom(16);
          marker.setPosition(place.geometry.location);

          const lat = place.geometry.location.lat();
          const lng = place.geometry.location.lng();
          let city = 'Pune';
          let state = 'Maharashtra';
          let postal = '';

          if (place.address_components) {
            for (const comp of place.address_components) {
              if (comp.types.includes('locality')) city = comp.long_name;
              if (comp.types.includes('administrative_area_level_1')) state = comp.long_name;
              if (comp.types.includes('postal_code')) postal = comp.long_name;
            }
          }

          const locObj = {
            address: place.formatted_address || place.name,
            latitude: lat,
            longitude: lng,
            city,
            state,
            postal_code: postal,
            place_id: place.place_id,
          };

          setCustomAddress(locObj.address);
          setCustomLat(lat);
          setCustomLng(lng);
          setIsConfirmed(true);
          onLocationSelect(locObj);
        });
      }
    } catch (err) {
      console.error('Google Maps initialization error:', err);
      setLoadError(true);
    }
  }, [mapsLoaded]);

  // Handle Preset Selection
  const handleSelectPreset = (corridor) => {
    setCustomAddress(corridor.address);
    setCustomLat(corridor.latitude);
    setCustomLng(corridor.longitude);
    setIsConfirmed(true);

    if (mapInstanceRef.current && markerInstanceRef.current && window.google) {
      const pos = { lat: corridor.latitude, lng: corridor.longitude };
      mapInstanceRef.current.setCenter(pos);
      mapInstanceRef.current.setZoom(15);
      markerInstanceRef.current.setPosition(pos);
    }

    onLocationSelect({
      address: corridor.address,
      latitude: corridor.latitude,
      longitude: corridor.longitude,
      city: corridor.city,
      state: corridor.state,
      name: corridor.name,
      type: corridor.type,
    });
  };

  // Manual confirmation of custom coordinates / address
  const handleManualConfirm = () => {
    setIsConfirmed(true);
    onLocationSelect({
      address: customAddress,
      latitude: parseFloat(customLat) || 18.756,
      longitude: parseFloat(customLng) || 73.4116,
      city: customAddress.split(',')[1]?.trim() || 'Pune',
      state: customAddress.split(',')[2]?.trim() || 'Maharashtra',
    });
  };

  const isLiveGoogleMaps = apiKey && mapsLoaded && !loadError;

  return (
    <div className="google-corridor-map-wrapper">
      {/* Header & Status Indicator */}
      <div className="map-panel-header">
        <div className="map-header-title">
          <span className="eyebrow">LOCATION & GIS CORRIDOR</span>
          <h3>Select Infrastructure on Google Maps</h3>
        </div>
        <div className="map-badge-pill">
          {isLiveGoogleMaps ? (
            <span className="live-status-pill green">
              <span className="pulse-dot" /> Google Maps API Active
            </span>
          ) : (
            <span className="live-status-pill amber" title="Add VITE_GOOGLE_MAPS_API_KEY to frontend/.env">
              📍 Indian Corridor Navigator
            </span>
          )}
        </div>
      </div>

      {/* Autocomplete / Corridor Search Bar */}
      <div className="map-search-row">
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            ref={searchInputRef}
            type="text"
            className="map-search-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search Indian city, road, bridge, junction (e.g. Pune, Bandra-Worli, ORR Bengaluru)..."
          />
          {searchQuery && (
            <button type="button" className="clear-search-btn" onClick={() => setSearchQuery('')}>
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Quick Indian Preset Corridors */}
      <div className="preset-corridors-row">
        <span className="preset-label">⚡ Fast Corridors:</span>
        <div className="preset-chips-scroll">
          {FALLBACK_CORRIDORS.slice(0, 5).map((c) => (
            <button
              key={c.name}
              type="button"
              className={`preset-chip ${selectedLocation?.address?.includes(c.city) || customAddress.includes(c.name) ? 'active' : ''}`}
              onClick={() => handleSelectPreset(c)}
            >
              {c.type === 'Bridge' ? '🌉' : '🛣️'} {c.name} ({c.city})
            </button>
          ))}
        </div>
      </div>

      {/* Google Maps Display Area */}
      {isLiveGoogleMaps ? (
        <div className="google-map-embed-frame">
          <div ref={mapContainerRef} className="google-map-canvas" style={{ width: '100%', height: '360px' }} />
          <div className="map-hint-overlay">
            <span>💡 Click map to place marker · Drag marker to adjust location</span>
          </div>
        </div>
      ) : (
        /* Graceful Fallback Mode: Clean, fully functioning Indian Corridor visual selector */
        <div className="fallback-corridor-map-card">
          <div className="fallback-config-banner">
            <span className="banner-icon">🗺️</span>
            <div>
              <strong>Interactive India Infrastructure Locator Active</strong>
              <p>
                Click any major corridor below or enter precise coordinates. To enable Google Maps Satellite & Street
                View, set <code>VITE_GOOGLE_MAPS_API_KEY</code> in <code>frontend/.env</code>.
              </p>
            </div>
          </div>

          {/* Interactive Indian Corridor Node Grid */}
          <div className="indian-corridor-grid">
            {FALLBACK_CORRIDORS.map((c) => (
              <div
                key={c.name}
                className={`corridor-node-card ${customAddress.includes(c.name) ? 'selected' : ''}`}
                onClick={() => handleSelectPreset(c)}
              >
                <div className="corridor-card-top">
                  <span className="node-icon">{c.type === 'Bridge' ? '🌉' : '🛣️'}</span>
                  <div>
                    <strong>{c.name}</strong>
                    <small>{c.city}, {c.state}</small>
                  </div>
                </div>
                <div className="corridor-coords-tag">
                  {c.latitude.toFixed(4)}°N, {c.longitude.toFixed(4)}°E
                </div>
              </div>
            ))}
          </div>

          {/* Manual Coordinate / Custom Location Bar */}
          <div className="manual-coord-row">
            <div className="coord-field">
              <label>Address / Landmark</label>
              <input
                type="text"
                value={customAddress}
                onChange={(e) => {
                  setCustomAddress(e.target.value);
                  setIsConfirmed(false);
                }}
                placeholder="Enter Indian address or corridor name"
              />
            </div>
            <div className="coord-field small">
              <label>Latitude</label>
              <input
                type="number"
                step="0.0001"
                value={customLat}
                onChange={(e) => {
                  setCustomLat(e.target.value);
                  setIsConfirmed(false);
                }}
              />
            </div>
            <div className="coord-field small">
              <label>Longitude</label>
              <input
                type="number"
                step="0.0001"
                value={customLng}
                onChange={(e) => {
                  setCustomLng(e.target.value);
                  setIsConfirmed(false);
                }}
              />
            </div>
            <button
              type="button"
              className={`apply-coord-btn ${isConfirmed ? 'confirmed' : ''}`}
              onClick={handleManualConfirm}
            >
              {isConfirmed ? '✓ Confirmed' : 'Update Location'}
            </button>
          </div>
        </div>
      )}

      {/* Selected Location Summary Card */}
      <div className="selected-location-summary panel">
        <div className="summary-icon-col">
          <span className="loc-pin-icon">📍</span>
        </div>
        <div className="summary-info-col">
          <div className="summary-eyebrow">CONFIRMED ASSESSMENT LOCATION</div>
          <h4 className="summary-address">{customAddress}</h4>
          <div className="summary-meta-row">
            <span>🌐 <strong>Latitude:</strong> {parseFloat(customLat).toFixed(4)}° N</span>
            <span>🌐 <strong>Longitude:</strong> {parseFloat(customLng).toFixed(4)}° E</span>
            <span className="region-badge">
              🇮🇳 India · {customAddress.includes('Maharashtra') ? 'West Zone' : customAddress.includes('Karnataka') ? 'South Zone' : 'National Civil Network'}
            </span>
          </div>
        </div>
        <div className="summary-action-col">
          <a
            href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(customAddress)}`}
            target="_blank"
            rel="noopener noreferrer"
            className="external-map-btn"
            title="Open in Google Maps"
          >
            Google Maps ↗
          </a>
        </div>
      </div>
    </div>
  );
}
