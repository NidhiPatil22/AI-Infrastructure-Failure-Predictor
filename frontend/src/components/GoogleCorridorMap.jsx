import { useEffect, useRef, useState } from 'react';

// Curated Major Indian Corridors & Landmarks for instant selection and testing
const POPULAR_INDIAN_CORRIDORS = [
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

// Dictionary of standard Indian city coordinates for instant local geocoding
const INDIAN_CITIES_COORDS = {
  pune: { lat: 18.5204, lng: 73.8567, state: 'Maharashtra', city: 'Pune' },
  mumbai: { lat: 19.076, lng: 72.8777, state: 'Maharashtra', city: 'Mumbai' },
  nagpur: { lat: 21.1458, lng: 79.0882, state: 'Maharashtra', city: 'Nagpur' },
  nashik: { lat: 19.9975, lng: 73.7898, state: 'Maharashtra', city: 'Nashik' },
  bengaluru: { lat: 12.9716, lng: 77.5946, state: 'Karnataka', city: 'Bengaluru' },
  bangalore: { lat: 12.9716, lng: 77.5946, state: 'Karnataka', city: 'Bengaluru' },
  hyderabad: { lat: 17.385, lng: 78.4867, state: 'Telangana', city: 'Hyderabad' },
  delhi: { lat: 28.6139, lng: 77.209, state: 'Delhi', city: 'New Delhi' },
  'new delhi': { lat: 28.6139, lng: 77.209, state: 'Delhi', city: 'New Delhi' },
  chennai: { lat: 13.0827, lng: 80.2707, state: 'Tamil Nadu', city: 'Chennai' },
  ahmedabad: { lat: 23.0225, lng: 72.5714, state: 'Gujarat', city: 'Ahmedabad' },
  kolkata: { lat: 22.5726, lng: 88.3639, state: 'West Bengal', city: 'Kolkata' },
  jaipur: { lat: 26.9124, lng: 75.7873, state: 'Rajasthan', city: 'Jaipur' },
  lucknow: { lat: 26.8467, lng: 80.9462, state: 'Uttar Pradesh', city: 'Lucknow' },
  chandigarh: { lat: 30.7333, lng: 76.7794, state: 'Punjab', city: 'Chandigarh' },
  thane: { lat: 19.2183, lng: 72.9781, state: 'Maharashtra', city: 'Thane' },
  'navi mumbai': { lat: 19.033, lng: 73.0297, state: 'Maharashtra', city: 'Navi Mumbai' },
  surat: { lat: 21.1702, lng: 72.8311, state: 'Gujarat', city: 'Surat' },
  indore: { lat: 22.7196, lng: 75.8577, state: 'Madhya Pradesh', city: 'Indore' },
  bhopal: { lat: 23.2599, lng: 77.4126, state: 'Madhya Pradesh', city: 'Bhopal' },
  kochi: { lat: 9.9312, lng: 76.2673, state: 'Kerala', city: 'Kochi' },
  coimbatore: { lat: 11.0168, lng: 76.9558, state: 'Tamil Nadu', city: 'Coimbatore' },
  visakhapatnam: { lat: 17.6868, lng: 83.2185, state: 'Andhra Pradesh', city: 'Visakhapatnam' },
  patna: { lat: 25.5941, lng: 85.1376, state: 'Bihar', city: 'Patna' },
};

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

  // Google Maps View controls
  const [mapType, setMapType] = useState('m'); // 'm' = Roadmap, 'k' = Satellite, 'p' = Terrain
  const [zoomLevel, setZoomLevel] = useState(15);
  const [useJsApi, setUseJsApi] = useState(Boolean(apiKey));

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
      setLoadError(false);
      return;
    }

    if (window.google && window.google.maps) {
      setMapsLoaded(true);
      return;
    }

    const existingScript = document.getElementById('google-maps-script');
    if (!existingScript) {
      const script = document.createElement('script');
      script.id = 'google-maps-script';
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setMapsLoaded(true);
      script.onerror = () => {
        console.warn('Google Maps script failed to load. Falling back to Google Maps Embed viewer.');
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
    if (!mapsLoaded || !mapContainerRef.current || !window.google || !window.google.maps || !useJsApi) return;

    try {
      const defaultCenter = {
        lat: parseFloat(customLat) || 18.756,
        lng: parseFloat(customLng) || 73.4116,
      };

      const map = new window.google.maps.Map(mapContainerRef.current, {
        center: defaultCenter,
        zoom: zoomLevel,
        mapTypeId: mapType === 'k' ? 'satellite' : mapType === 'p' ? 'terrain' : 'roadmap',
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

      const marker = new window.google.maps.Marker({
        position: defaultCenter,
        map,
        title: customAddress || 'Selected Infrastructure Location',
        animation: window.google.maps.Animation.DROP,
        draggable: true,
      });
      markerInstanceRef.current = marker;

      const geocoder = new window.google.maps.Geocoder();

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

      map.addListener('click', (e) => {
        const lat = e.latLng.lat();
        const lng = e.latLng.lng();
        marker.setPosition(e.latLng);
        updateFromLatLng(lat, lng);
      });

      marker.addListener('dragend', (e) => {
        const lat = e.latLng.lat();
        const lng = e.latLng.lng();
        updateFromLatLng(lat, lng);
      });

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
  }, [mapsLoaded, useJsApi]);

  // Handle Preset Selection
  const handleSelectPreset = (corridor) => {
    setCustomAddress(corridor.address);
    setCustomLat(corridor.latitude);
    setCustomLng(corridor.longitude);
    setIsConfirmed(true);

    if (mapInstanceRef.current && markerInstanceRef.current && window.google && useJsApi) {
      const pos = { lat: corridor.latitude, lng: corridor.longitude };
      mapInstanceRef.current.setCenter(pos);
      mapInstanceRef.current.setZoom(zoomLevel);
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

  // Handle location search by query text (works with or without Places API)
  const handlePerformSearch = (e) => {
    if (e) e.preventDefault();
    const query = searchQuery.trim();
    if (!query) return;

    const queryLower = query.toLowerCase();

    // 1. Check if user typed coordinates like "18.756, 73.4116"
    const coordMatch = query.match(/^([-+]?\d{1,2}(?:\.\d+)?)\s*,\s*([-+]?\d{1,3}(?:\.\d+)?)$/);
    if (coordMatch) {
      const lat = parseFloat(coordMatch[1]);
      const lng = parseFloat(coordMatch[2]);
      const addr = `Custom Coordinates: ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E, India`;
      setCustomLat(lat);
      setCustomLng(lng);
      setCustomAddress(addr);
      setIsConfirmed(true);
      onLocationSelect({
        address: addr,
        latitude: lat,
        longitude: lng,
        city: 'Pune',
        state: 'Maharashtra',
      });
      return;
    }

    // 2. Check if matched against popular Indian corridors
    const matchedCorridor = POPULAR_INDIAN_CORRIDORS.find(
      (c) =>
        c.name.toLowerCase().includes(queryLower) ||
        c.city.toLowerCase().includes(queryLower) ||
        c.address.toLowerCase().includes(queryLower)
    );

    if (matchedCorridor) {
      handleSelectPreset(matchedCorridor);
      return;
    }

    // 3. Check if matched against known Indian cities
    for (const [cityName, info] of Object.entries(INDIAN_CITIES_COORDS)) {
      if (queryLower.includes(cityName)) {
        const addr = `${query}, ${info.city}, ${info.state}, India`;
        setCustomLat(info.lat);
        setCustomLng(info.lng);
        setCustomAddress(addr);
        setIsConfirmed(true);
        onLocationSelect({
          address: addr,
          latitude: info.lat,
          longitude: info.lng,
          city: info.city,
          state: info.state,
        });
        return;
      }
    }

    // 4. Default: Treat as Indian address
    const fullAddr = query.toLowerCase().includes('india') ? query : `${query}, India`;
    setCustomAddress(fullAddr);
    setIsConfirmed(true);
    onLocationSelect({
      address: fullAddr,
      latitude: customLat,
      longitude: customLng,
      city: 'Pune',
      state: 'Maharashtra',
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

  const isLiveJsMapsActive = apiKey && mapsLoaded && !loadError && useJsApi;

  // Compute live Google Maps Embed URL
  const encodedQuery = encodeURIComponent(
    customAddress && customAddress.length > 5
      ? customAddress
      : `${parseFloat(customLat).toFixed(4)},${parseFloat(customLng).toFixed(4)}`
  );
  const googleMapsEmbedUrl = `https://maps.google.com/maps?q=${encodedQuery}&t=${mapType}&z=${zoomLevel}&ie=UTF8&iwloc=&output=embed`;

  return (
    <div className="google-corridor-map-wrapper">
      {/* Header & Status Indicator */}
      <div className="map-panel-header">
        <div className="map-header-title">
          <span className="eyebrow">LOCATION & GIS CORRIDOR</span>
          <h3>Select Infrastructure on Google Maps</h3>
        </div>
        <div className="map-badge-pill">
          {apiKey ? (
            <button
              type="button"
              className={`live-status-pill ${isLiveJsMapsActive ? 'green' : 'amber'}`}
              onClick={() => setUseJsApi(!useJsApi)}
              title="Click to toggle between Dynamic JS Map and Google Maps Embed"
            >
              <span className="pulse-dot" /> {isLiveJsMapsActive ? 'Google Maps JS Active' : 'Google Maps Live Embed'}
            </button>
          ) : (
            <span className="live-status-pill green">
              <span className="pulse-dot" /> Live Google Maps Connected
            </span>
          )}
        </div>
      </div>

      {/* Autocomplete / Corridor Search Bar */}
      <form className="map-search-row" onSubmit={handlePerformSearch}>
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            ref={searchInputRef}
            type="text"
            className="map-search-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search Indian road, bridge, junction (e.g. Bandra-Worli, Pune, Bengaluru ORR)..."
          />
          {searchQuery && (
            <button type="button" className="clear-search-btn" onClick={() => setSearchQuery('')}>
              ✕
            </button>
          )}
          <button type="submit" className="search-submit-btn">
            Locate
          </button>
        </div>
      </form>

      {/* Quick Indian Preset Corridors */}
      <div className="preset-corridors-row">
        <span className="preset-label">⚡ Fast Corridors:</span>
        <div className="preset-chips-scroll">
          {POPULAR_INDIAN_CORRIDORS.slice(0, 5).map((c) => (
            <button
              key={c.name}
              type="button"
              className={`preset-chip ${customAddress.includes(c.name) ? 'active' : ''}`}
              onClick={() => handleSelectPreset(c)}
            >
              {c.type === 'Bridge' ? '🌉' : '🛣️'} {c.name} ({c.city})
            </button>
          ))}
        </div>
      </div>

      {/* Map Layer & Zoom Controls Toolbar */}
      <div className="map-controls-toolbar">
        <div className="map-type-toggles">
          <button
            type="button"
            className={`map-tool-btn ${mapType === 'm' ? 'active' : ''}`}
            onClick={() => setMapType('m')}
            title="Roadmap & Highway Network"
          >
            🗺️ Roadmap
          </button>
          <button
            type="button"
            className={`map-tool-btn ${mapType === 'k' ? 'active' : ''}`}
            onClick={() => setMapType('k')}
            title="Satellite Aerial Imagery"
          >
            🛰️ Satellite
          </button>
          <button
            type="button"
            className={`map-tool-btn ${mapType === 'p' ? 'active' : ''}`}
            onClick={() => setMapType('p')}
            title="Topographical Terrain"
          >
            ⛰️ Terrain
          </button>
        </div>

        <div className="map-zoom-toggles">
          <span className="zoom-label">Zoom: {zoomLevel}x</span>
          <button
            type="button"
            className="zoom-btn"
            onClick={() => setZoomLevel((prev) => Math.max(10, prev - 1))}
            title="Zoom Out"
          >
            -
          </button>
          <button
            type="button"
            className="zoom-btn"
            onClick={() => setZoomLevel((prev) => Math.min(19, prev + 1))}
            title="Zoom In"
          >
            +
          </button>
        </div>
      </div>

      {/* VISIBLE GOOGLE MAP DISPLAY CANVAS */}
      <div className="google-map-embed-frame">
        {isLiveJsMapsActive ? (
          <div ref={mapContainerRef} className="google-map-canvas" style={{ width: '100%', height: '380px' }} />
        ) : (
          <iframe
            key={`${encodedQuery}-${mapType}-${zoomLevel}`}
            title="Google Maps Corridor Live View"
            width="100%"
            height="380"
            style={{
              border: 0,
              borderRadius: '10px',
              display: 'block',
              backgroundColor: '#0b131e',
            }}
            loading="lazy"
            allowFullScreen
            referrerPolicy="no-referrer-when-downgrade"
            src={googleMapsEmbedUrl}
          />
        )}

        <div className="map-hint-overlay">
          <span>📍 Pin Location: <strong>{customAddress.split(',')[0]}</strong></span>
          <a
            href={`https://www.google.com/maps/search/?api=1&query=${encodedQuery}`}
            target="_blank"
            rel="noopener noreferrer"
            className="mini-maps-link"
          >
            Open in Google Maps ↗
          </a>
        </div>
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
          {isConfirmed ? '✓ Confirmed' : 'Update Pin'}
        </button>
      </div>

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
