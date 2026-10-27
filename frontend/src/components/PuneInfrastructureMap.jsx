import { useCallback, useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getInfrastructure, getInfrastructureAssetDetail, getDamageReports } from '../services/api.js';
import InfrastructureDetailsPanel from './InfrastructureDetailsPanel.jsx';

// Pune Municipal Center & Bounding Constraints
const PUNE_CENTER = [18.5204, 73.8567];
const PUNE_BOUNDS = [
  [18.4100, 73.7300], // South-West
  [18.6500, 73.9900], // North-East
];

const PUNE_WARDS = [
  'All Wards',
  'Kothrud Ward',
  'Shivajinagar-Ghole Road Ward',
  'Aundh-Baner Ward',
  'Hadapsar-Mundhwa Ward',
  'Dhankawadi-Sahakarnagar Ward',
  'Bhosari MIDC Ward',
  'Kasba-Vishrambaug Wada Ward',
  'Nagar Road-Vadgaonsheri Ward',
  'Bibwewadi Ward',
];

const ASSET_TYPES = [
  'All Types',
  'Road Segment',
  'Bridge Approach',
  'Culvert Approach',
  'Road',
  'Bridge',
];

// Helper to create HTML marker icons
function createAssetMarkerIcon(asset) {
  const risk = String(asset.risk_level || 'LOW').toUpperCase();
  const hasDamage = (asset.reported_damage_count || 0) > 0;

  let color = '#10b981'; // green
  let glow = 'rgba(16, 185, 129, 0.3)';
  let symbol = '●';

  if (hasDamage || risk === 'CRITICAL') {
    color = '#ef4444';
    glow = 'rgba(239, 68, 68, 0.6)';
    symbol = '⚠️';
  } else if (risk === 'HIGH') {
    color = '#f87171';
    glow = 'rgba(248, 113, 113, 0.4)';
    symbol = '▲';
  } else if (risk === 'MEDIUM') {
    color = '#f59e0b';
    glow = 'rgba(245, 158, 11, 0.3)';
    symbol = '■';
  }

  return L.divIcon({
    className: 'custom-infra-marker',
    html: `
      <div style="
        position: relative;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      ">
        <div style="
          position: absolute;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: ${glow};
          ${hasDamage || risk === 'HIGH' ? 'animation: pulseGlow 1.8s infinite ease-out;' : ''}
        "></div>
        <div style="
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: #0f172a;
          border: 2px solid ${color};
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 8px;
          color: ${color};
          font-weight: bold;
          box-shadow: 0 2px 6px rgba(0,0,0,0.6);
        ">
          ${symbol}
        </div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
}

function createDamagePinIcon(report) {
  return L.divIcon({
    className: 'damage-pin-marker',
    html: `
      <div style="
        position: relative;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      ">
        <div style="
          position: absolute;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: rgba(239, 68, 68, 0.4);
          animation: pulseGlow 1.5s infinite;
        "></div>
        <div style="
          width: 26px;
          height: 26px;
          border-radius: 50%;
          background: #7f1d1d;
          border: 2px solid #fecb00;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 13px;
          box-shadow: 0 4px 10px rgba(0,0,0,0.7);
        ">
          ⚠️
        </div>
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });
}

export default function PuneInfrastructureMap({ onSelectLocation, pickMode = false }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);
  const damageLayerRef = useRef(null);
  const pickMarkerRef = useRef(null);
  const tileLayersRef = useRef({});
  const activeTileLayerRef = useRef(null);

  // Map Base Layer State (Google Maps Default)
  const [mapLayer, setMapLayer] = useState('googleRoad');

  // Filters State
  const [selectedType, setSelectedType] = useState('All Types');
  const [selectedRisk, setSelectedRisk] = useState('all');
  const [selectedWard, setSelectedWard] = useState('All Wards');
  const [showDamageReports, setShowDamageReports] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  // Data & Selection State
  const [assets, setAssets] = useState([]);
  const [damageReports, setDamageReports] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [selectedDamageReport, setSelectedDamageReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [totalMonitored, setTotalMonitored] = useState(50000);

  // Initialize Leaflet Map Centered on Pune with Google Maps
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapInstanceRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: PUNE_CENTER,
      zoom: 12,
      minZoom: 11,
      maxZoom: 19,
      maxBounds: PUNE_BOUNDS,
      maxBoundsViscosity: 0.8,
    });

    // 1. Google Maps Road Map (Standard Pune Street Network)
    const googleRoadLayer = L.tileLayer(
      'https://mt{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
      {
        subdomains: ['0', '1', '2', '3'],
        attribution: '&copy; Google Maps & Pune Municipal Corporation',
        maxZoom: 20,
      }
    );

    // 2. Google Maps Hybrid (Satellite Imagery + Street Labels)
    const googleSatelliteLayer = L.tileLayer(
      'https://mt{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
      {
        subdomains: ['0', '1', '2', '3'],
        attribution: '&copy; Google Maps & Pune Municipal Corporation',
        maxZoom: 20,
      }
    );

    // 3. Google Maps Terrain (Physical Elevation, Hills, Contours & Drainage)
    const googleTerrainLayer = L.tileLayer(
      'https://mt{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
      {
        subdomains: ['0', '1', '2', '3'],
        attribution: '&copy; Google Maps & Pune Municipal Corporation',
        maxZoom: 20,
      }
    );

    // 4. OpenStreetMap High-Contrast Road Backup
    const osmLayer = L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        attribution: '&copy; OpenStreetMap contributors & Pune Municipal Corporation',
        maxZoom: 19,
      }
    );

    tileLayersRef.current = {
      googleRoad: googleRoadLayer,
      googleSatellite: googleSatelliteLayer,
      googleTerrain: googleTerrainLayer,
      osm: osmLayer,
    };

    // Default to Google Maps Road
    googleRoadLayer.addTo(map);
    activeTileLayerRef.current = googleRoadLayer;

    // City Bounding Polygon Guide (Pune Monitored Sector)
    const boundsPoly = L.rectangle(PUNE_BOUNDS, {
      color: '#fecb00',
      weight: 1.5,
      fill: true,
      fillColor: '#fecb00',
      fillOpacity: 0.03,
      dashArray: '4, 8',
    }).addTo(map);

    const markersLayer = L.layerGroup().addTo(map);
    const damageLayer = L.layerGroup().addTo(map);

    markersLayerRef.current = markersLayer;
    damageLayerRef.current = damageLayer;
    mapInstanceRef.current = map;

    // Pick location event for damage report submission
    map.on('click', (e) => {
      const { lat, lng } = e.latlng;
      if (
        lat < PUNE_BOUNDS[0][0] ||
        lat > PUNE_BOUNDS[1][0] ||
        lng < PUNE_BOUNDS[0][1] ||
        lng > PUNE_BOUNDS[1][1]
      ) {
        alert('Please click inside the Pune municipal monitoring boundary (yellow dashed sector).');
        return;
      }

      if (onSelectLocation) {
        onSelectLocation({ latitude: Number(lat.toFixed(6)), longitude: Number(lng.toFixed(6)) });
      }

      if (pickMode) {
        if (pickMarkerRef.current) {
          pickMarkerRef.current.setLatLng(e.latlng);
        } else {
          pickMarkerRef.current = L.marker(e.latlng, {
            icon: L.divIcon({
              className: 'pick-pin',
              html: '<div style="font-size:24px; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.8));">📍</div>',
              iconSize: [24, 24],
              iconAnchor: [12, 24],
            }),
          }).addTo(map);
        }
      }
    });

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [onSelectLocation, pickMode]);

  // Handle Layer Switching (Google Maps Road / Satellite / Terrain / OSM)
  useEffect(() => {
    if (!mapInstanceRef.current || !tileLayersRef.current) return;
    const map = mapInstanceRef.current;
    const newLayer = tileLayersRef.current[mapLayer];
    if (newLayer && newLayer !== activeTileLayerRef.current) {
      if (activeTileLayerRef.current) {
        map.removeLayer(activeTileLayerRef.current);
      }
      newLayer.addTo(map);
      newLayer.bringToBack();
      activeTileLayerRef.current = newLayer;
    }
  }, [mapLayer]);

  // Fetch Assets from Backend with Viewport & Filters
  const fetchMapData = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        limit: 800, // Balanced viewport rendering
      };

      if (selectedType !== 'All Types') params.type = selectedType;
      if (selectedRisk !== 'all') params.risk = selectedRisk;
      if (selectedWard !== 'All Wards') params.ward = selectedWard;
      if (searchQuery.trim()) params.search = searchQuery.trim();

      const [infraRes, damageRes] = await Promise.all([
        getInfrastructure(params),
        getDamageReports({ limit: 40 }),
      ]);

      const fetchedAssets = Array.isArray(infraRes?.assets) ? infraRes.assets : [];
      setAssets(fetchedAssets);
      setTotalMonitored(infraRes?.total || 100000);
      setDamageReports(Array.isArray(damageRes?.reports) ? damageRes.reports : []);
    } catch (err) {
      console.error('Failed to load map infrastructure:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedType, selectedRisk, selectedWard, searchQuery]);

  useEffect(() => {
    fetchMapData();
  }, [fetchMapData]);

  // Update Leaflet Markers when Assets or Damage Reports change
  useEffect(() => {
    const map = mapInstanceRef.current;
    const markersLayer = markersLayerRef.current;
    const damageLayer = damageLayerRef.current;
    if (!map || !markersLayer || !damageLayer) return;

    markersLayer.clearLayers();
    damageLayer.clearLayers();

    // 1. Add Monitored Assets Markers
    assets.forEach((asset) => {
      if (!asset.latitude || !asset.longitude) return;

      const marker = L.marker([asset.latitude, asset.longitude], {
        icon: createAssetMarkerIcon(asset),
      });

      marker.on('click', async () => {
        try {
          const detail = await getInfrastructureAssetDetail(asset.asset_id);
          setSelectedAsset(detail);
        } catch {
          setSelectedAsset(asset);
        }
        setSelectedDamageReport(null);
      });

      const roadClass = asset.road_class ? asset.road_class.charAt(0).toUpperCase() + asset.road_class.slice(1) : '';
      const typeLabel = (asset.asset_type || 'Road Segment').replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
      const fullType = roadClass ? `${roadClass} ${typeLabel}` : typeLabel;
      const condition = asset.condition_label || (asset.condition_score < 50 ? 'Poor' : (asset.condition_score < 75 ? 'Fair' : 'Good'));
      const rulDays = asset.remaining_useful_life_days != null
        ? `${asset.remaining_useful_life_days} days`
        : (asset.remaining_useful_life != null ? `${Math.round(Number(asset.remaining_useful_life) > 100 ? Number(asset.remaining_useful_life) : Number(asset.remaining_useful_life) * 365)} days` : 'N/A');
      const locality = asset.locality || asset.pune_ward || 'Pune';

      marker.bindTooltip(
        `<div style="font-family: inherit; font-size: 11px; line-height: 1.45; min-width: 130px;">
          <div style="font-weight: 700; color: #fecb00; margin-bottom: 2px;">${fullType}</div>
          <div><strong>Risk:</strong> <span style="font-weight: 700; color: ${asset.risk_level === 'HIGH' || asset.risk_level === 'CRITICAL' ? '#ef4444' : '#10b981'};">${asset.risk_level || 'LOW'}</span></div>
          <div><strong>Condition:</strong> ${condition}</div>
          <div><strong>RUL:</strong> ${rulDays}</div>
          <div><strong>Locality:</strong> ${locality}</div>
          ${(asset.reported_damage_count || 0) > 0 ? `<div style="color: #ef4444; font-weight: 600; margin-top: 2px;">⚠️ ${asset.reported_damage_count} Damage Report(s)</div>` : ''}
        </div>`,
        { direction: 'top', offset: [0, -10] }
      );

      markersLayer.addLayer(marker);
    });

    // 2. Add Damage Reports Layer
    if (showDamageReports) {
      damageReports.forEach((rep) => {
        if (!rep.latitude || !rep.longitude) return;

        const dmgMarker = L.marker([rep.latitude, rep.longitude], {
          icon: createDamagePinIcon(rep),
        });

        dmgMarker.on('click', () => {
          setSelectedDamageReport(rep);
          setSelectedAsset(null);
        });

        dmgMarker.bindTooltip(
          `<strong>Field Damage: ${rep.damage_type}</strong><br/>${rep.report_id} · ${rep.status}`,
          { direction: 'top', offset: [0, -12] }
        );

        damageLayer.addLayer(dmgMarker);
      });
    }
  }, [assets, damageReports, showDamageReports]);

  const resetFilters = () => {
    setSelectedType('All Types');
    setSelectedRisk('all');
    setSelectedWard('All Wards');
    setSearchQuery('');
  };

  const highRiskCount = assets.filter((a) => String(a.risk_level).toUpperCase() === 'HIGH').length;

  return (
    <div className="pune-map-viewport-wrapper">
      {/* 1. Map Filter Toolbar */}
      <div className="map-controls-toolbar">
        <div className="map-filter-group">
          <label className="toolbar-search">
            <span>⌕</span>
            <input
              type="text"
              placeholder="Search locality, road class, or ward..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </label>

          <select
            className="toolbar-select"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            aria-label="Filter by Infrastructure Type"
          >
            {ASSET_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>

          <select
            className="toolbar-select"
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            aria-label="Filter by Risk Tier"
          >
            <option value="all">All Risk Tiers</option>
            <option value="high">High Risk Only</option>
            <option value="medium">Medium Risk</option>
            <option value="low">Low Risk / Stable</option>
          </select>

          <select
            className="toolbar-select"
            value={selectedWard}
            onChange={(e) => setSelectedWard(e.target.value)}
            aria-label="Filter by Pune Municipal Ward"
          >
            {PUNE_WARDS.map((w) => (
              <option key={w} value={w}>
                {w}
              </option>
            ))}
          </select>

          <button
            type="button"
            className={`damage-toggle-btn ${showDamageReports ? 'active' : ''}`}
            onClick={() => setShowDamageReports((prev) => !prev)}
            title="Toggle Field Damage Inspection Markers"
          >
            ⚠️ Damage Reports ({damageReports.length})
          </button>

          {/* Map Base Layer Selector (Google Maps / Satellite / Terrain / OSM) */}
          <select
            className="toolbar-select layer-select"
            value={mapLayer}
            onChange={(e) => setMapLayer(e.target.value)}
            aria-label="Map Base Layer"
            style={{ fontWeight: 600, borderColor: '#fecb00' }}
          >
            <option value="googleRoad">🗺️ Google Maps (Roads)</option>
            <option value="googleSatellite">🛰️ Google Satellite Hybrid</option>
            <option value="googleTerrain">🏔️ Google Terrain</option>
            <option value="osm">🌐 OpenStreetMap</option>
          </select>

          <button type="button" className="secondary-button reset-btn" onClick={resetFilters}>
            Reset Filters
          </button>
        </div>

        {/* Dynamic Map Statistics Banner */}
        <div className="map-stats-strip">
          <span className="stat-pill">
            Showing <strong>{assets.length.toLocaleString()}</strong> / {totalMonitored.toLocaleString()} assets
          </span>
          <span className="stat-pill highlight-red">
            High Risk: <strong>{highRiskCount}</strong>
          </span>
          <span className="stat-pill highlight-amber">
            Damage Reports: <strong>{damageReports.length}</strong>
          </span>
          {loading && <span className="stat-pill loading-pill">Syncing telemetry...</span>}
        </div>
      </div>

      {/* 2. Leaflet Map Element Container */}
      <div className="map-canvas-container" style={{ position: 'relative', width: '100%', height: '620px' }}>
        <div ref={mapContainerRef} style={{ width: '100%', height: '100%', background: '#0b131e' }} />

        {/* Map Legend Overlay */}
        <div className="map-legend-box">
          <strong>PUNE GIS LEGEND</strong>
          <div className="legend-item">
            <span className="legend-dot red" /> High Risk (Prob ≥ 70%)
          </div>
          <div className="legend-item">
            <span className="legend-dot amber" /> Medium Risk (Prob 35-70%)
          </div>
          <div className="legend-item">
            <span className="legend-dot green" /> Low Risk (Prob &lt; 35%)
          </div>
          <div className="legend-item">
            <span className="legend-icon">⚠️</span> Field Damage Report
          </div>
        </div>

        {/* Selected Damage Report Modal Card */}
        {selectedDamageReport && (
          <div className="damage-popup-card">
            <div className="popup-header">
              <span className="popup-eyebrow">FIELD DAMAGE INSPECTION</span>
              <button
                type="button"
                className="popup-close-btn"
                onClick={() => setSelectedDamageReport(null)}
              >
                ✕
              </button>
            </div>
            <h4>{selectedDamageReport.damage_type}</h4>
            <div className="popup-meta">
              <span>Report ID: <strong>{selectedDamageReport.report_id}</strong></span>
              <span>Status: <strong className="text-accent">{selectedDamageReport.status}</strong></span>
              <span>Ward: {selectedDamageReport.pune_ward || 'Pune Sector'}</span>
              {selectedDamageReport.associated_asset_id && (
                <span>
                  Linked Asset:{' '}
                  <button
                    type="button"
                    className="link-button"
                    onClick={async () => {
                      try {
                        const asset = await getInfrastructureAssetDetail(
                          selectedDamageReport.associated_asset_id
                        );
                        setSelectedAsset(asset);
                        setSelectedDamageReport(null);
                      } catch (e) {
                        console.error(e);
                      }
                    }}
                  >
                    {selectedDamageReport.associated_asset_id}
                  </button>
                </span>
              )}
            </div>
            {selectedDamageReport.cv_detected && (
              <div className="popup-cv-note">
                AI CV Analysis: <strong>{selectedDamageReport.cv_detected}</strong>
                {selectedDamageReport.cv_confidence && (
                  <small> ({(selectedDamageReport.cv_confidence * 100).toFixed(0)}% confidence)</small>
                )}
              </div>
            )}
            {selectedDamageReport.image_url && (
              <img
                src={selectedDamageReport.image_url}
                alt="Damage inspection"
                className="popup-damage-img"
              />
            )}
            <p className="popup-desc">{selectedDamageReport.description}</p>
          </div>
        )}
      </div>

      {/* 3. Detailed Infrastructure Monitoring Drawer Panel */}
      {selectedAsset && (
        <InfrastructureDetailsPanel
          asset={selectedAsset}
          onClose={() => setSelectedAsset(null)}
        />
      )}
    </div>
  );
}

function round(val, dec = 4) {
  const p = Math.pow(10, dec);
  return Math.round(val * p) / p;
}
