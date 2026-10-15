import { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

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

// Custom Pulsing Highway Marker Icon for Leaflet
const createHighwayPinIcon = () =>
  L.divIcon({
    className: 'custom-highway-pin',
    html: `
      <div style="position: relative; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;">
        <div style="position: absolute; width: 36px; height: 36px; border-radius: 50%; background: rgba(254, 203, 0, 0.4); animation: pinPulse 2s infinite ease-out;"></div>
        <div style="position: absolute; width: 28px; height: 28px; border-radius: 50%; background: #0b131e; border: 2.5px solid #fecb00; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5); font-size: 14px;">
          📍
        </div>
      </div>
    `,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -20],
  });

export default function GoogleCorridorMap({ selectedLocation, onLocationSelect }) {
  const mapElementRef = useRef(null);
  const leafletMapRef = useRef(null);
  const markerRef = useRef(null);
  const baseLayersRef = useRef({});

  const [customLat, setCustomLat] = useState(selectedLocation?.latitude || 18.756);
  const [customLng, setCustomLng] = useState(selectedLocation?.longitude || 73.4116);
  const [customAddress, setCustomAddress] = useState(
    selectedLocation?.address || 'Mumbai - Pune Expressway, Maharashtra, India'
  );
  const [searchQuery, setSearchQuery] = useState('');
  const [isConfirmed, setIsConfirmed] = useState(true);

  // 3 Primary View Modes:
  // 1. 'satellite' -> Real Photorealistic Satellite Imagery & Surroundings
  // 2. 'road'      -> Clear Road, Highway & Corridor Street Network
  // 3. 'terrain'   -> Topography, Elevation Contours & Physical Landscape
  const [activeViewMode, setActiveViewMode] = useState('satellite');

  // Sync state if selectedLocation prop changes from parent
  useEffect(() => {
    if (selectedLocation) {
      if (selectedLocation.address) setCustomAddress(selectedLocation.address);
      if (selectedLocation.latitude) setCustomLat(selectedLocation.latitude);
      if (selectedLocation.longitude) setCustomLng(selectedLocation.longitude);
    }
  }, [selectedLocation]);

  // Reverse Geocoding helper using OpenStreetMap Nominatim
  const reverseGeocode = async (lat, lng) => {
    try {
      const resp = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=16&addressdetails=1`,
        { headers: { 'Accept-Language': 'en' } }
      );
      if (resp.ok) {
        const data = await resp.json();
        const addr = data.display_name || `Location at ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E, India`;
        const city =
          data.address?.city ||
          data.address?.town ||
          data.address?.suburb ||
          data.address?.county ||
          'Pune';
        const state = data.address?.state || 'Maharashtra';
        const postal = data.address?.postcode || '';

        const locObj = {
          address: addr,
          latitude: lat,
          longitude: lng,
          city,
          state,
          postal_code: postal,
          place_id: data.place_id,
        };

        setCustomAddress(addr);
        setCustomLat(lat);
        setCustomLng(lng);
        setIsConfirmed(true);
        onLocationSelect(locObj);
        return locObj;
      }
    } catch (err) {
      console.warn('Reverse geocoding error:', err);
    }

    // Fallback if network offline
    const fallbackAddr = `Coordinates: ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E, Maharashtra, India`;
    setCustomAddress(fallbackAddr);
    setCustomLat(lat);
    setCustomLng(lng);
    setIsConfirmed(true);
    onLocationSelect({
      address: fallbackAddr,
      latitude: lat,
      longitude: lng,
      city: 'Pune',
      state: 'Maharashtra',
    });
  };

  // Initialize Leaflet Map with the 3 Distinct High-Quality View Layers
  useEffect(() => {
    if (!mapElementRef.current || leafletMapRef.current) return;

    const initialLat = parseFloat(customLat) || 18.756;
    const initialLng = parseFloat(customLng) || 73.4116;

    // 1. Satellite View Layer: Ultra-High Resolution Esri World Imagery (Surroundings, Trees, Buildings, Water)
    const satelliteLayer = L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        maxZoom: 19,
      }
    );

    // Overlay for Satellite View: Highway & City Labels
    const labelsOverlay = L.tileLayer(
      'https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
      {
        maxZoom: 19,
        opacity: 0.9,
      }
    );

    // Combined Satellite Group (Satellite + Road Labels)
    const satelliteGroup = L.layerGroup([satelliteLayer, labelsOverlay]);

    // 2. Road Network View Layer: High-Contrast OpenStreetMap Civil Roads & Corridors
    const roadLayer = L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }
    );

    // 3. Topography & Terrain View Layer: Physical Elevation, Hills, Contours & Drainage
    const terrainLayer = L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
      {
        attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
        maxZoom: 19,
      }
    );

    baseLayersRef.current = {
      satellite: satelliteGroup,
      road: roadLayer,
      terrain: terrainLayer,
    };

    // Instantiate map with default Satellite Surroundings view
    const map = L.map(mapElementRef.current, {
      center: [initialLat, initialLng],
      zoom: 15,
      layers: [satelliteGroup],
      zoomControl: false,
    });
    leafletMapRef.current = map;

    // Zoom control at bottom right
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Add Pulsing Pin Marker at initial location
    const marker = L.marker([initialLat, initialLng], {
      icon: createHighwayPinIcon(),
      draggable: true,
    }).addTo(map);
    markerRef.current = marker;

    marker.bindPopup(
      `<div style="font-family: inherit; font-size: 12px; color: #0b131e;">
        <strong>Selected Civil Asset</strong><br/>
        ${customAddress.split(',')[0]}
      </div>`
    );

    // Click map to reposition marker and reverse-geocode
    map.on('click', (e) => {
      const { lat, lng } = e.latlng;
      marker.setLatLng([lat, lng]);
      marker.openPopup();
      reverseGeocode(lat, lng);
    });

    // Marker drag end
    marker.on('dragend', (e) => {
      const { lat, lng } = e.target.getLatLng();
      reverseGeocode(lat, lng);
    });

    return () => {
      map.remove();
      leafletMapRef.current = null;
    };
  }, []);

  // Switch between the 3 View Types
  const handleSwitchView = (mode) => {
    setActiveViewMode(mode);
    const map = leafletMapRef.current;
    if (!map || !baseLayersRef.current) return;

    // Remove existing layers
    Object.values(baseLayersRef.current).forEach((layer) => {
      if (map.hasLayer(layer)) {
        map.removeLayer(layer);
      }
    });

    // Add selected layer
    const selectedLayer = baseLayersRef.current[mode];
    if (selectedLayer) {
      map.addLayer(selectedLayer);
    }
  };

  // Fly to location helper
  const flyToCoords = (lat, lng, address) => {
    setCustomLat(lat);
    setCustomLng(lng);
    if (address) setCustomAddress(address);
    setIsConfirmed(true);

    if (leafletMapRef.current && markerRef.current) {
      leafletMapRef.current.flyTo([lat, lng], 16, { duration: 1.2 });
      markerRef.current.setLatLng([lat, lng]);
      markerRef.current.setPopupContent(
        `<div style="font-family: inherit; font-size: 12px; color: #0b131e;">
          <strong>${address ? address.split(',')[0] : 'Selected Infrastructure'}</strong><br/>
          ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E
        </div>`
      );
    }
  };

  // Handle Preset Corridor Click
  const handleSelectPreset = (corridor) => {
    flyToCoords(corridor.latitude, corridor.longitude, corridor.address);

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

  // Handle Search Input Submit
  const handlePerformSearch = (e) => {
    if (e) e.preventDefault();
    const query = searchQuery.trim();
    if (!query) return;

    const queryLower = query.toLowerCase();

    // 1. Check if user typed numeric coordinates: "18.756, 73.4116"
    const coordMatch = query.match(/^([-+]?\d{1,2}(?:\.\d+)?)\s*,\s*([-+]?\d{1,3}(?:\.\d+)?)$/);
    if (coordMatch) {
      const lat = parseFloat(coordMatch[1]);
      const lng = parseFloat(coordMatch[2]);
      const addr = `Custom Coordinates: ${lat.toFixed(4)}°N, ${lng.toFixed(4)}°E, India`;
      flyToCoords(lat, lng, addr);
      onLocationSelect({
        address: addr,
        latitude: lat,
        longitude: lng,
        city: 'Pune',
        state: 'Maharashtra',
      });
      return;
    }

    // 2. Check if query matches popular corridor presets
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

    // 3. Check if query matches known Indian city coordinates
    for (const [cityName, info] of Object.entries(INDIAN_CITIES_COORDS)) {
      if (queryLower.includes(cityName)) {
        const addr = `${query}, ${info.city}, ${info.state}, India`;
        flyToCoords(info.lat, info.lng, addr);
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

    // 4. Default: Query OpenStreetMap Nominatim for Indian places
    fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        query + ', India'
      )}&limit=1`,
      { headers: { 'Accept-Language': 'en' } }
    )
      .then((res) => res.json())
      .then((results) => {
        if (results && results.length > 0) {
          const first = results[0];
          const lat = parseFloat(first.lat);
          const lng = parseFloat(first.lon);
          const addr = first.display_name;
          flyToCoords(lat, lng, addr);
          onLocationSelect({
            address: addr,
            latitude: lat,
            longitude: lng,
            city: addr.split(',')[1]?.trim() || 'Pune',
            state: addr.split(',')[2]?.trim() || 'Maharashtra',
          });
        } else {
          // Fallback
          const fullAddr = query.toLowerCase().includes('india') ? query : `${query}, India`;
          setCustomAddress(fullAddr);
          setIsConfirmed(true);
        }
      })
      .catch((err) => {
        console.warn('Geocoding search failed:', err);
      });
  };

  // Manual coordinate input apply
  const handleManualConfirm = () => {
    const lat = parseFloat(customLat) || 18.756;
    const lng = parseFloat(customLng) || 73.4116;
    flyToCoords(lat, lng, customAddress);
    onLocationSelect({
      address: customAddress,
      latitude: lat,
      longitude: lng,
      city: customAddress.split(',')[1]?.trim() || 'Pune',
      state: customAddress.split(',')[2]?.trim() || 'Maharashtra',
    });
  };

  return (
    <div className="google-corridor-map-wrapper">
      {/* Header & Status Indicator */}
      <div className="map-panel-header">
        <div className="map-header-title">
          <span className="eyebrow">LOCATION-AWARE GIS CORRIDOR</span>
          <h3>Explore Infrastructure in 3 Views</h3>
        </div>
        <div className="map-badge-pill">
          <span className="live-status-pill green">
            <span className="pulse-dot" /> High-Res GIS Aerial Connected
          </span>
        </div>
      </div>

      {/* Autocomplete / Corridor Search Bar */}
      <form className="map-search-row" onSubmit={handlePerformSearch}>
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
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

      {/* 3 DISTINCT VIEW MODES SELECTOR */}
      <div className="three-views-selector-bar">
        <button
          type="button"
          className={`view-mode-card ${activeViewMode === 'satellite' ? 'active' : ''}`}
          onClick={() => handleSwitchView('satellite')}
        >
          <span className="view-card-icon">🛰️</span>
          <div className="view-card-info">
            <strong>1. Satellite & Surroundings</strong>
            <small>Photorealistic aerial view of buildings, trees & surroundings</small>
          </div>
          {activeViewMode === 'satellite' && <span className="view-active-pill">ACTIVE</span>}
        </button>

        <button
          type="button"
          className={`view-mode-card ${activeViewMode === 'road' ? 'active' : ''}`}
          onClick={() => handleSwitchView('road')}
        >
          <span className="view-card-icon">🛣️</span>
          <div className="view-card-info">
            <strong>2. Road & Highway Network</strong>
            <small>Civil corridor lanes, expressways, street lines & bridges</small>
          </div>
          {activeViewMode === 'road' && <span className="view-active-pill">ACTIVE</span>}
        </button>

        <button
          type="button"
          className={`view-mode-card ${activeViewMode === 'terrain' ? 'active' : ''}`}
          onClick={() => handleSwitchView('terrain')}
        >
          <span className="view-card-icon">⛰️</span>
          <div className="view-card-info">
            <strong>3. Topography & Terrain</strong>
            <small>Elevation slope, relief contours & drainage watershed</small>
          </div>
          {activeViewMode === 'terrain' && <span className="view-active-pill">ACTIVE</span>}
        </button>
      </div>

      {/* INTERACTIVE MAP CANVAS */}
      <div className="google-map-embed-frame">
        <div ref={mapElementRef} style={{ width: '100%', height: '390px', borderRadius: '10px' }} />

        {/* View Mode Tag & Hint */}
        <div className="map-hint-overlay">
          <span>
            📍 <strong>{customAddress.split(',')[0]}</strong> &bull; Click anywhere on map to reposition pin
          </span>
          <span className="layer-mode-badge">
            {activeViewMode === 'satellite' ? '🛰️ Satellite Imagery' : activeViewMode === 'road' ? '🛣️ Road Map' : '⛰️ Topography'}
          </span>
        </div>
      </div>

      {/* 360° Surroundings & Full Map Action Links */}
      <div className="surroundings-actions-bar">
        <a
          href={`https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${parseFloat(customLat).toFixed(6)},${parseFloat(customLng).toFixed(6)}&heading=0&pitch=0&fov=80`}
          target="_blank"
          rel="noopener noreferrer"
          className="surroundings-action-btn street-view"
          title="Inspect actual roadside surroundings, pavement & civil condition in 360°"
        >
          👀 Inspect 360° Street Surroundings (Google Street View) ↗
        </a>
        <a
          href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(customAddress)}`}
          target="_blank"
          rel="noopener noreferrer"
          className="surroundings-action-btn maps-link"
          title="Open in Google Maps for live traffic"
        >
          🗺️ Open in Google Maps ↗
        </a>
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
              🇮🇳 India &bull; {customAddress.includes('Maharashtra') ? 'West Zone' : customAddress.includes('Karnataka') ? 'South Zone' : 'National Civil Network'}
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
