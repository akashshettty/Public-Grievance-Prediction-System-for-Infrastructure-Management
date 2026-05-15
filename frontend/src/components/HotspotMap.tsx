import React, { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'

// Fix for default marker icons in Leaflet
import icon from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})
L.Marker.prototype.options.icon = DefaultIcon

interface HotspotMapProps {
  predictions: any[]
}

const HotspotMap: React.FC<HotspotMapProps> = ({ predictions }) => {
  const [geoData, setGeoData] = useState<any>(null)

  useEffect(() => {
    fetch('/BBMP.geojson')
      .then(res => res.json())
      .then(data => setGeoData(data))
      .catch(err => console.error('Error loading GeoJSON:', err))
  }, [])

  // Map predictions to ward numbers for easy lookup
  const predictionMap = predictions.reduce((acc: any, p: any) => {
    const wardNum = p.ward.match(/\d+/)?.[0]
    if (wardNum) {
      acc[wardNum] = p
    }
    return acc
  }, {})

  const style = (feature: any) => {
    const wardNo = feature.properties.KGISWardNo
    const prediction = predictionMap[wardNo]
    
    let color = '#94A3B8' // Default soft slate
    let weight = 1
    let fillOpacity = 0.2

    if (prediction) {
      const prob = prediction.failure_probability
      // More vibrant colors
      if (prediction.risk_level.toLowerCase() === 'critical') color = '#F43F5E' // Vibrant Rose
      else if (prediction.risk_level.toLowerCase() === 'high') color = '#F59E0B' // Amber
      else color = '#10B981' // Emerald
      
      weight = 3
      fillOpacity = 0.7 + (prob * 0.2)
    }

    return {
      fillColor: color,
      weight: weight,
      opacity: 1,
      color: color,
      fillOpacity: fillOpacity
    }
  }

  const onEachFeature = (feature: any, layer: any) => {
    const wardNo = feature.properties.KGISWardNo
    const wardName = feature.properties.KGISWardName
    const prediction = predictionMap[wardNo]

    let popupContent = `
      <div style="color: black; min-width: 150px;">
        <h3 style="margin: 0 0 5px 0; border-bottom: 1px solid #eee; padding-bottom: 5px;">${wardName}</h3>
        <p style="margin: 5px 0;">Ward Number: <strong>${wardNo}</strong></p>
    `

    if (prediction) {
      popupContent += `
        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
          <p style="margin: 0; color: #666; font-size: 11px;">FAILURE PROBABILITY</p>
          <p style="margin: 0; font-size: 20px; font-weight: bold; color: ${prediction.risk_level.toLowerCase() === 'critical' ? '#ff006e' : '#333'}">
            ${(prediction.failure_probability * 100).toFixed(1)}%
          </p>
          <p style="margin: 5px 0 0 0; font-size: 12px;">Risk Level: <span style="text-transform: uppercase; font-weight: bold;">${prediction.risk_level}</span></p>
          <p style="margin: 2px 0 0 0; font-size: 12px;">Est. Date: ${prediction.predicted_date || prediction.forecast_date}</p>
        </div>
      `
    } else {
      popupContent += `<p style="margin: 10px 0 0 0; font-size: 12px; color: #999;">No high-risk hotspots predicted for this area.</p>`
    }

    popupContent += `</div>`
    layer.bindPopup(popupContent)

    layer.on({
      mouseover: (e: any) => {
        const layer = e.target
        layer.setStyle({
          fillOpacity: 0.9,
          weight: 3
        })
      },
      mouseout: (e: any) => {
        const layer = e.target
        layer.setStyle(style(feature))
      }
    })
  }

  if (!geoData) {
    return <div className="h-[500px] flex items-center justify-center text-white/50">Loading Geographical Data...</div>
  }

  return (
    <div className="rounded-2xl overflow-hidden border border-white/10 shadow-2xl relative h-[600px]">
      <MapContainer 
        center={[12.9716, 77.5946]} 
        zoom={11} 
        style={{ height: '100%', width: '100%', background: '#000' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />
        <GeoJSON 
          data={geoData} 
          style={style}
          onEachFeature={onEachFeature}
        />
      </MapContainer>

      {/* Legend */}
      <div className="absolute bottom-6 right-6 z-[1000] glass-dark p-4 rounded-xl border border-white/10">
        <h4 className="text-xs font-bold text-gray-400 mb-3 uppercase tracking-wider">Hotspot Intensity</h4>
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-[#ff006e] shadow-[0_0_10px_rgba(255,0,110,0.5)]"></div>
            <span className="text-sm text-gray-200">Critical Risk (&gt;80%)</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-[#ffd700] shadow-[0_0_10px_rgba(255,215,0,0.5)]"></div>
            <span className="text-sm text-gray-200">High Risk (60-80%)</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-[#00d9ff] shadow-[0_0_10px_rgba(0,217,255,0.5)]"></div>
            <span className="text-sm text-gray-200">Moderate Risk</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-[#333]"></div>
            <span className="text-sm text-gray-400">Baseline/Stable</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HotspotMap
